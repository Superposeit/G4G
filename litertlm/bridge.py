# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fastapi[standard]>=0.136.0",
#     "litert-lm-nightly>=0.11.0.dev20260418",
#     "uvicorn>=0.44.0",
# ]
# ///

"""
LiteRT-LM OpenAI-Compatible Bridge

Provides an OpenAI-compatible HTTP API for LiteRT-LM models, enabling
integration with tools that expect OpenAI's /v1/chat/completions endpoint.

Features:
- OpenAI-compatible streaming responses
- Text-only support (vision/audio disabled due to library limitations)
- Configurable model path and settings
- Health check endpoint
- Error handling with detailed logging

Environment Variables:
    LITERTLM_MODEL_PATH: Path to .litertlm model file (required)
    LITERTLM_HOST: Host to bind to (default: 0.0.0.0)
    LITERTLM_PORT: Port to bind to (default: 8000)
    LITERTLM_MODEL_ID: Model ID to report (default: gemma-4-E2B-it)
    LITERTLM_LOG_LEVEL: Logging level (default: INFO)

Note: Vision and audio support are currently disabled due to signature
limitations in litert-lm-nightly. The bridge supports text-only inference.
"""

import os
import sys
import logging
import json
import re
import threading
import time
from typing import Any, Dict, Generator, List, Optional, Union

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Resolve project root relative to this file (litertlm/bridge.py → project root)
# and ensure it is importable so ``litertlm.engines`` resolves both when this
# file runs as a script (``uv run bridge.py``) and when imported as a module.
# NOTE: ``litert_lm`` is intentionally NOT imported here — it is loaded lazily
# inside the engine's ``start()`` so this module imports without the library.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from litertlm.engines import EngineSupervisor, LiteRTEngine  # noqa: E402

# --- Configuration ---

# Run `python scripts/download_litertlm_model.py` to populate the default path.
_DEFAULT_MODEL_PATH = os.path.join(
    _PROJECT_ROOT, "data", "models", "gemma-4-E2B-it.litertlm"
)

# Environment variables with defaults
MODEL_PATH = os.environ.get("LITERTLM_MODEL_PATH", _DEFAULT_MODEL_PATH)
HOST = os.environ.get("LITERTLM_HOST", "0.0.0.0")
PORT = int(os.environ.get("LITERTLM_PORT", "8000"))

# These are no longer constants as they can be updated dynamically
_current_model_id = os.environ.get("LITERTLM_MODEL_ID", "gemma-4-E2B-it")
_current_model_path = os.environ.get("LITERTLM_MODEL_PATH", str(_DEFAULT_MODEL_PATH))
LOG_LEVEL = os.environ.get("LITERTLM_LOG_LEVEL", "INFO")

# --- Logging Setup ---

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("litertlm-bridge")

# --- Engine Manager ---

# Global supervisor instance (lazy loaded). Owns the active chat engine plus any
# optional ASR / embedding engines.
_supervisor: Optional[EngineSupervisor] = None
_engine_lock = threading.Lock()


def get_supervisor() -> EngineSupervisor:
    """Get or create the :class:`EngineSupervisor` (lazy).

    The default configuration preserves the historical bridge behaviour: an
    in-process, text-only LiteRT-LM chat engine and no auxiliary engines
    (endpoints that need ASR/embeddings return 503 until one is configured).
    Heavy work — importing ``litert_lm`` and loading the model — happens inside
    the engine's ``start()``, driven on first use. Tests replace this module
    global with a fake so no real engine is ever constructed.
    """
    global _supervisor

    if _supervisor is not None:
        return _supervisor

    with _engine_lock:
        # Double-check after acquiring lock
        if _supervisor is not None:
            return _supervisor

        logger.info(f"Configuring engine manager (default model: {_current_model_path})")
        chat_engine = LiteRTEngine(
            model_path=_current_model_path, model_id=_current_model_id
        )
        _supervisor = EngineSupervisor(tier="lite", chat_engine=chat_engine)
        return _supervisor


# --- FastAPI App ---

app = FastAPI(
    title="LiteRT-LM Bridge",
    description="OpenAI-compatible API for LiteRT-LM models",
    version="1.0.0"
)


# --- Helper Functions ---

def parse_multimodal_content(openai_content: str | List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Converts OpenAI-style message content (text or list of parts)
    into LiteRT-LM compatible parts.

    Args:
        openai_content: Either a string or a list of content parts

    Returns:
        List of LiteRT-LM compatible content parts
    """
    if isinstance(openai_content, str):
        return [{"type": "text", "text": openai_content}]

    parts = []
    for item in openai_content:
        if item["type"] == "text":
            parts.append({"type": "text", "text": item["text"]})

        elif item["type"] == "image_url":
            url = item["image_url"]["url"]
            # Extract base64 data from Data URI (data:image/jpeg;base64,...)
            base64_data = re.sub(r'^data:image/.+;base64,', '', url)
            parts.append({"type": "image", "blob": base64_data})

        elif item["type"] == "input_audio":
            parts.append({"type": "audio", "blob": item["input_audio"]["data"]})

        else:
            logger.warning(f"Unsupported content type: {item['type']}")

    return parts


def format_sse_chunk(data: Dict[str, Any]) -> str:
    """Format data as Server-Sent Events chunk."""
    return f"data: {json.dumps(data)}\n\n"


def format_error_chunk(message: str, error_type: str = "runtime_error") -> str:
    """Format error as SSE chunk."""
    error_data = {"error": {"message": message, "type": error_type}}
    return format_sse_chunk(error_data)


# --- API Endpoints ---

@app.get("/v1/models")
async def list_models() -> Dict[str, Any]:
    """List available models (OpenAI-compatible)."""
    return {
        "object": "list",
        "data": [{
            "id": _current_model_id,
            "object": "model",
            "created": int(time.time()),
            "owned_by": "litert-community"
        }]
    }


@app.get("/")
@app.get("/v1")
async def root() -> Dict[str, str]:
    """Root endpoint for health check."""
    return {"status": "LiteRT-LM Multimodal Bridge is running", "model": _current_model_id}


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    try:
        # Ensure the chat engine is started and ready.
        supervisor = get_supervisor()
        engine = supervisor.get_chat_engine()
        if engine is None or not engine.health():
            raise RuntimeError("Chat engine is not ready")
        return {
            "status": "healthy",
            "model": _current_model_id,
            "model_path": _current_model_path
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


class SetModelRequest(BaseModel):
    model_path: str
    model_id: str

@app.post("/v1/models/active")
async def set_active_model(request: SetModelRequest) -> Dict[str, str]:
    """Change the active chat model dynamically without restarting."""
    global _current_model_id, _current_model_path

    if not os.path.exists(request.model_path):
        raise HTTPException(status_code=404, detail="Model file not found")

    # Resolve the supervisor outside the lock (it manages its own locking).
    supervisor = get_supervisor()

    with _engine_lock:
        try:
            logger.info(f"Switching model to: {request.model_path}")
            _current_model_path = request.model_path
            _current_model_id = request.model_id

            # Hot-swap: stop the old chat engine and start a fresh LiteRT engine.
            new_engine = LiteRTEngine(
                model_path=_current_model_path, model_id=_current_model_id
            )
            supervisor.swap_chat_engine(new_engine)

            return {
                "status": "success",
                "message": f"Successfully switched to model {request.model_id}"
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to switch model: {e}")
            raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/chat/completions")
async def chat_completions(request: Request) -> StreamingResponse:
    """
    OpenAI-compatible chat completions endpoint with streaming support.

    Args:
        request: FastAPI request object

    Returns:
        StreamingResponse with SSE-formatted chunks
    """
    try:
        body = await request.json()
        messages = body.get("messages", [])

        if not messages:
            raise HTTPException(status_code=400, detail="No messages provided")

        logger.debug(f"Received request with {len(messages)} messages")

        # Forward optional OpenAI generation parameters to the active engine.
        # Message-format handling (history/multimodal) is owned by the engine so
        # the bridge stays engine-agnostic across LiteRT and llama.cpp.
        opts = {
            k: body[k]
            for k in ("temperature", "top_p", "top_k", "max_tokens", "stop", "seed")
            if k in body
        }

        def generate_stream() -> Generator[str, None, None]:
            """Stream the active engine's output as OpenAI-compatible SSE chunks."""
            try:
                supervisor = get_supervisor()
                engine = supervisor.get_chat_engine()
                if engine is None:
                    raise RuntimeError("No chat engine is configured on this node")

                for text in engine.chat(messages, **opts):
                    if text:
                        data = {
                            "id": f"chatcmpl-{int(time.time())}",
                            "object": "chat.completion.chunk",
                            "model": _current_model_id,
                            "choices": [{
                                "delta": {"content": text},
                                "finish_reason": None,
                                "index": 0
                            }]
                        }
                        yield format_sse_chunk(data)

                # Final stop signal to tell the UI the model is done
                stop_data = {
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion.chunk",
                    "model": _current_model_id,
                    "choices": [{"delta": {}, "finish_reason": "stop", "index": 0}]
                }
                yield format_sse_chunk(stop_data)
                yield "data: [DONE]\n\n"

                logger.debug("Generation completed successfully")

            except FileNotFoundError as e:
                logger.error(f"Model file not found: {e}")
                yield format_error_chunk(str(e), "file_not_found")
                yield "data: [DONE]\n\n"
            except Exception as e:
                logger.error(f"Generation error: {e}", exc_info=True)
                yield format_error_chunk(str(e), "runtime_error")
                yield "data: [DONE]\n\n"

        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )

    except HTTPException:
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in request: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")
    except Exception as e:
        logger.error(f"Unexpected error in chat_completions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


class EmbeddingsRequest(BaseModel):
    input: Union[str, List[str]]
    model: Optional[str] = None


@app.post("/v1/embeddings")
async def create_embeddings(request: EmbeddingsRequest) -> Dict[str, Any]:
    """OpenAI-compatible embeddings endpoint.

    Delegates to the supervisor's embedding engine. Returns 503 when no
    embedding-capable engine is loaded on this node.
    """
    supervisor = get_supervisor()
    engine = supervisor.get_embedding_engine()
    if engine is None:
        raise HTTPException(
            status_code=503,
            detail="No embedding engine is loaded on this node."
        )

    texts = [request.input] if isinstance(request.input, str) else list(request.input)
    try:
        vectors = engine.embed(texts)
    except NotImplementedError:
        raise HTTPException(
            status_code=503,
            detail="The active engine does not support embeddings."
        )

    return {
        "object": "list",
        "data": [
            {"object": "embedding", "index": i, "embedding": vector}
            for i, vector in enumerate(vectors)
        ],
        "model": request.model or _current_model_id,
        "usage": {"prompt_tokens": 0, "total_tokens": 0},
    }


@app.post("/v1/audio/transcriptions")
async def create_transcription(request: Request) -> Dict[str, str]:
    """OpenAI-compatible audio transcription endpoint.

    Delegates to the supervisor's ASR engine. Returns a clear 503 when no ASR
    engine is loaded on this node.
    """
    supervisor = get_supervisor()
    engine = supervisor.get_asr_engine()
    if engine is None:
        raise HTTPException(
            status_code=503,
            detail="No ASR engine is loaded on this node."
        )

    audio = await request.body()
    try:
        text = engine.transcribe(audio)
    except NotImplementedError:
        raise HTTPException(
            status_code=503,
            detail="The active engine does not support audio transcription."
        )

    return {"text": text}


# --- Main Entry Point ---

if __name__ == "__main__":
    import uvicorn

    logger.info(f"🚀 LiteRT Multimodal Bridge starting on http://{HOST}:{PORT}")
    logger.info(f"   Model: {_current_model_id}")
    logger.info(f"   Model path: {_current_model_path}")
    logger.info(f"   Log level: {LOG_LEVEL}")

    uvicorn.run(app, host=HOST, port=PORT)

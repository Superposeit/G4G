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
import logging
import json
import re
import threading
import time
from typing import Any, Dict, List, Generator, Optional

import litert_lm
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import uvicorn

# ============================================
# Configuration
# ============================================

# Resolve project root relative to this file (litertlm/bridge.py → project root).
# Run `python scripts/download_litertlm_model.py` to populate the default path.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_MODEL_PATH = os.path.join(
    _PROJECT_ROOT, "data", "models", "gemma-4-E2B-it.litertlm"
)

# Environment variables with defaults
MODEL_PATH = os.environ.get("LITERTLM_MODEL_PATH", _DEFAULT_MODEL_PATH)
HOST = os.environ.get("LITERTLM_HOST", "0.0.0.0")
PORT = int(os.environ.get("LITERTLM_PORT", "8000"))
MODEL_ID = os.environ.get("LITERTLM_MODEL_ID", "gemma-4-E2B-it")
LOG_LEVEL = os.environ.get("LITERTLM_LOG_LEVEL", "INFO")

# ============================================
# Logging Setup
# ============================================

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("litertlm-bridge")

# ============================================
# Model Initialization
# ============================================

# Global engine instance (lazy loaded)
_engine: Optional[Any] = None
_engine_lock = threading.Lock()
# Request lock to ensure only one conversation session exists at a time (LiteRT limitation)
_request_lock = threading.Lock()


def get_engine() -> Any:
    """Get or create the LiteRT-LM engine instance (lazy loading)."""
    global _engine

    if _engine is not None:
        return _engine

    with _engine_lock:
        # Double-check after acquiring lock
        if _engine is not None:
            return _engine

        logger.info(f"Loading model from: {MODEL_PATH}")

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. "
                f"Run 'python scripts/download_litertlm_model.py' to download the model."
            )

        try:
            # Initialize Engine (text-only for now)
            # Note: Vision and audio backends disabled due to signature limitation
            # in current litert-lm-nightly version
            _engine = litert_lm.Engine(MODEL_PATH)
            logger.info("Model loaded successfully")
            return _engine
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise


# ============================================
# FastAPI App
# ============================================

app = FastAPI(
    title="LiteRT-LM Bridge",
    description="OpenAI-compatible API for LiteRT-LM models",
    version="1.0.0"
)


# ============================================
# Helper Functions
# ============================================

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


# ============================================
# API Endpoints
# ============================================

@app.get("/v1/models")
async def list_models() -> Dict[str, Any]:
    """List available models (OpenAI-compatible)."""
    return {
        "object": "list",
        "data": [{
            "id": MODEL_ID,
            "object": "model",
            "created": int(time.time()),
            "owned_by": "litert-community"
        }]
    }


@app.get("/")
@app.get("/v1")
async def root() -> Dict[str, str]:
    """Root endpoint for health check."""
    return {"status": "LiteRT-LM Multimodal Bridge is running", "model": MODEL_ID}


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    try:
        # Try to get engine to verify it's loaded
        engine = get_engine()
        return {
            "status": "healthy",
            "model": MODEL_ID,
            "model_path": MODEL_PATH
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


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

        # 1. Prepare History (OpenAI format to LiteRT format)
        # We pass all but the last message as context
        history = []
        for m in messages[:-1]:
            content = m["content"]
            # If content is a string, use it directly
            # If it's a list, check if it's text-only
            if isinstance(content, str):
                history.append({"role": m["role"], "content": content})
            elif isinstance(content, list):
                # Check if it's text-only (single text part)
                if len(content) == 1 and content[0]["type"] == "text":
                    history.append({"role": m["role"], "content": content[0]["text"]})
                else:
                    # Multimodal - convert to LiteRT format
                    history.append({"role": m["role"], "content": parse_multimodal_content(content)})
            else:
                history.append({"role": m["role"], "content": str(content)})

        # 2. Prepare Current Prompt
        last_content = messages[-1]["content"]
        if isinstance(last_content, str):
            user_message = last_content
        elif isinstance(last_content, list):
            if len(last_content) == 1 and last_content[0]["type"] == "text":
                user_message = last_content[0]["text"]
            else:
                # Extract text from multimodal content
                user_message = ""
                for item in last_content:
                    if item["type"] == "text":
                        user_message += item["text"]
        else:
            user_message = str(last_content)

        def generate_stream() -> Generator[str, None, None]:
            """Generate streaming response using LiteRT-LM."""
            try:
                engine = get_engine()

                # Use the lock to prevent 'FAILED_PRECONDITION: A session already exists'
                with _request_lock:
                    logger.debug("Acquired request lock, starting generation")

                    # Create conversation with history context
                    with engine.create_conversation(messages=history) as conversation:
                        for chunk in conversation.send_message_async(user_message):

                            # Extract text from the LiteRT content array
                            content = ""
                            for item in chunk.get("content", []):
                                if item.get("type") == "text":
                                    content += item.get("text", "")

                            if content:
                                data = {
                                    "id": f"chatcmpl-{int(time.time())}",
                                    "object": "chat.completion.chunk",
                                    "model": MODEL_ID,
                                    "choices": [{
                                        "delta": {"content": content},
                                        "finish_reason": None,
                                        "index": 0
                                    }]
                                }
                                yield format_sse_chunk(data)

                    # Final stop signal to tell the UI the model is done
                    stop_data = {
                        "id": f"chatcmpl-{int(time.time())}",
                        "object": "chat.completion.chunk",
                        "model": MODEL_ID,
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

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in request: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")
    except Exception as e:
        logger.error(f"Unexpected error in chat_completions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# Main Entry Point
# ============================================

if __name__ == "__main__":
    logger.info(f"🚀 LiteRT Multimodal Bridge starting on http://{HOST}:{PORT}")
    logger.info(f"   Model: {MODEL_ID}")
    logger.info(f"   Model path: {MODEL_PATH}")
    logger.info(f"   Log level: {LOG_LEVEL}")

    uvicorn.run(app, host=HOST, port=PORT)

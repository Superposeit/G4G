# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "fastapi[standard]>=0.136.0",
#     "litert-lm-nightly>=0.11.0.dev20260418",
#     "uvicorn>=0.44.0",
# ]
# ///

import os
import litert_lm
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import uvicorn
import json
import time
import threading
import re

app = FastAPI()

# Resolve project root relative to this file (litertlm/bridge.py → project root).
# Run  python scripts/download_litertlm_model.py  to populate the default path.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_MODEL_PATH = os.path.join(
    _PROJECT_ROOT, "data", "models", "gemma-4-E2B-it.litertlm"
)

# LITERTLM_MODEL_PATH env var is the canonical override.
# docker-compose mounts the host path as /model.litertlm and sets this var automatically.
MODEL_PATH = os.environ.get("LITERTLM_MODEL_PATH", _DEFAULT_MODEL_PATH)

# Initialize Engine with Multimodal Backends
# Note: Using CPU for vision/audio as it is most stable for WSL nightly builds
engine = litert_lm.Engine(
    MODEL_PATH,
    vision_backend=litert_lm.Backend.CPU,
    audio_backend=litert_lm.Backend.CPU
)

# Global lock to ensure only one conversation session exists at a time (LiteRT limitation)
engine_lock = threading.Lock()

def parse_multimodal_content(openai_content):
    """
    Converts OpenAI-style message content (text or list of parts)
    into LiteRT-LM compatible parts.
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

    return parts

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [{
            "id": "gemma-4-E2B-it",
            "object": "model",
            "created": int(time.time()),
            "owned_by": "litert-community"
        }]
    }

@app.get("/")
@app.get("/v1")
async def root():
    return {"status": "LiteRT-LM Multimodal Bridge is running"}

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    messages = body.get("messages", [])

    if not messages:
        return {"error": "No messages provided"}

    # 1. Prepare History (OpenAI format to LiteRT format)
    # We pass all but the last message as context
    history = []
    for m in messages[:-1]:
        history.append({
            "role": m["role"],
            "content": parse_multimodal_content(m["content"])
        })

    # 2. Prepare Current Prompt
    user_parts = parse_multimodal_content(messages[-1]["content"])

    def generate_stream():
        # Use the lock to prevent 'FAILED_PRECONDITION: A session already exists'
        with engine_lock:
            try:
                # Create conversation with history context
                with engine.create_conversation(messages=history) as conversation:
                    for chunk in conversation.send_message_async(user_parts):

                        # Extract text from the LiteRT content array
                        content = ""
                        for item in chunk.get("content", []):
                            if item.get("type") == "text":
                                content += item.get("text", "")

                        if content:
                            data = {
                                "id": "chatcmpl-litert",
                                "object": "chat.completion.chunk",
                                "model": "gemma-4-E2B-it",
                                "choices": [{
                                    "delta": {"content": content},
                                    "finish_reason": None,
                                    "index": 0
                                }]
                            }
                            yield f"data: {json.dumps(data)}\n\n"

                    # Final stop signal to tell the UI the model is done
                    stop_data = {
                        "id": "chatcmpl-litert",
                        "object": "chat.completion.chunk",
                        "model": "gemma-4-E2B-it",
                        "choices": [{"delta": {}, "finish_reason": "stop", "index": 0}]
                    }
                    yield f"data: {json.dumps(stop_data)}\n\n"
                    yield "data: [DONE]\n\n"
            except Exception as e:
                error_data = {"error": {"message": str(e), "type": "runtime_error"}}
                yield f"data: {json.dumps(error_data)}\n\n"
                yield "data: [DONE]\n\n"

    return StreamingResponse(generate_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    print("🚀 LiteRT Multimodal Bridge starting on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

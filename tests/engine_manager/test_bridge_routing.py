"""Routing tests for the bridge FastAPI app with engines faked out.

The supervisor is monkeypatched onto the module global so no real ``litert_lm``
library, GGUF model or engine binary is ever needed.
"""

from __future__ import annotations

import json
from typing import Optional

import pytest
from fastapi.testclient import TestClient

import litertlm.bridge as bridge


class FakeChatEngine:
    def __init__(self, chunks: list[str]) -> None:
        self._chunks = chunks

    def health(self) -> bool:
        return True

    def chat(self, messages, **opts):
        for chunk in self._chunks:
            yield chunk


class FakeEmbeddingEngine:
    def embed(self, texts):
        return [[0.1, 0.2] for _ in texts]


class FakeASREngine:
    def transcribe(self, audio, **opts) -> str:
        return "transcribed text"


class FakeSupervisor:
    def __init__(self, chat=None, embedding=None, asr=None) -> None:
        self._chat = chat
        self._embedding = embedding
        self._asr = asr

    def get_chat_engine(self, ensure_started: bool = True):
        return self._chat

    def get_embedding_engine(self):
        return self._embedding

    def get_asr_engine(self):
        return self._asr


def _client(monkeypatch: pytest.MonkeyPatch, supervisor: FakeSupervisor) -> TestClient:
    monkeypatch.setattr(bridge, "_supervisor", supervisor)
    return TestClient(bridge.app)


def _parse_sse_content(text: str) -> tuple[list[str], bool, bool]:
    """Return (content deltas, saw_stop, saw_done) from an SSE stream body."""
    contents: list[str] = []
    saw_stop = False
    saw_done = False
    for line in text.splitlines():
        if not line.startswith("data:"):
            continue
        payload = line[len("data:"):].strip()
        if payload == "[DONE]":
            saw_done = True
            continue
        obj = json.loads(payload)
        choice = obj["choices"][0]
        delta = choice.get("delta", {})
        if delta.get("content"):
            contents.append(delta["content"])
        if choice.get("finish_reason") == "stop":
            saw_stop = True
    return contents, saw_stop, saw_done


def test_health_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _client(monkeypatch, FakeSupervisor(chat=FakeChatEngine([])))
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "healthy"
    assert body["model"] == bridge._current_model_id


def test_root_endpoints(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _client(monkeypatch, FakeSupervisor(chat=FakeChatEngine([])))
    for path in ("/", "/v1"):
        resp = client.get(path)
        assert resp.status_code == 200
        assert "model" in resp.json()


def test_list_models_shape(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _client(monkeypatch, FakeSupervisor(chat=FakeChatEngine([])))
    resp = client.get("/v1/models")
    assert resp.status_code == 200
    body = resp.json()
    assert body["object"] == "list"
    assert isinstance(body["data"], list) and body["data"]
    entry = body["data"][0]
    assert entry["id"] == bridge._current_model_id
    assert entry["object"] == "model"
    assert entry["owned_by"] == "litert-community"


def test_chat_completions_streams_fake_chunks(monkeypatch: pytest.MonkeyPatch) -> None:
    supervisor = FakeSupervisor(chat=FakeChatEngine(["Hello", " world"]))
    client = _client(monkeypatch, supervisor)

    resp = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "hi"}]},
    )
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/event-stream")

    contents, saw_stop, saw_done = _parse_sse_content(resp.text)
    assert contents == ["Hello", " world"]
    assert saw_stop is True
    assert saw_done is True


def test_chat_completions_empty_messages_400(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _client(monkeypatch, FakeSupervisor(chat=FakeChatEngine([])))
    resp = client.post("/v1/chat/completions", json={"messages": []})
    assert resp.status_code == 400


def test_embeddings_returns_vectors(monkeypatch: pytest.MonkeyPatch) -> None:
    supervisor = FakeSupervisor(
        chat=FakeChatEngine([]), embedding=FakeEmbeddingEngine()
    )
    client = _client(monkeypatch, supervisor)

    resp = client.post("/v1/embeddings", json={"input": ["a", "b"]})
    assert resp.status_code == 200
    body = resp.json()
    assert body["object"] == "list"
    assert len(body["data"]) == 2
    assert body["data"][0]["embedding"] == [0.1, 0.2]
    assert body["data"][1]["index"] == 1


def test_embeddings_503_without_engine(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _client(monkeypatch, FakeSupervisor(chat=FakeChatEngine([]), embedding=None))
    resp = client.post("/v1/embeddings", json={"input": "hello"})
    assert resp.status_code == 503


def test_transcriptions_503_without_asr(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _client(monkeypatch, FakeSupervisor(chat=FakeChatEngine([]), asr=None))
    resp = client.post("/v1/audio/transcriptions", content=b"audio-bytes")
    assert resp.status_code == 503
    assert "ASR" in resp.json()["detail"]


def test_transcriptions_ok_with_asr(monkeypatch: pytest.MonkeyPatch) -> None:
    supervisor = FakeSupervisor(chat=FakeChatEngine([]), asr=FakeASREngine())
    client = _client(monkeypatch, supervisor)
    resp = client.post("/v1/audio/transcriptions", content=b"audio-bytes")
    assert resp.status_code == 200
    assert resp.json()["text"] == "transcribed text"

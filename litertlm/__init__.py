"""LiteRT-LM bridge package.

Hosts the OpenAI-compatible FastAPI bridge (``bridge.py``) and the dual-engine
"Engine Manager" (``engines`` subpackage). Importing this package MUST NOT pull
in ``litert_lm`` or any engine binary — all heavy imports are deferred so the
service remains importable and unit-testable on machines without them.
"""

__all__ = ["engines"]

"""
TutorRD Capability — EducaT / TutorRD
======================================

Tutor adaptativo de matemáticas para estudiantes dominicanos.
Implementa pedagogía socrática alineada al currículo MINERD, grados 3–9.

Sigue el mismo patrón que deep_solve.py: delega el LLM a stream_synthesis
y usa context.user_message / context.config_overrides.
"""

from __future__ import annotations

import json
from pathlib import Path

from deeptutor.core.capability_protocol import BaseCapability, CapabilityManifest
from deeptutor.core.context import UnifiedContext
from deeptutor.core.stream_bus import StreamBus

# ── Directorio de skills pedagógicos ──────────────────────────────────────────
SKILLS_DIR = Path(__file__).parent / "skills"


def _load_skill(skill_name: str) -> str:
    """Lee el SKILL.md del skill indicado."""
    path = SKILLS_DIR / skill_name / "SKILL.md"
    if not path.exists():
        return f"[SKILL '{skill_name}' no encontrado en {path}]"
    return path.read_text(encoding="utf-8")


def _seleccionar_skills(mensaje: str, historial: list[dict]) -> list[str]:
    """
    Decide qué 1–2 skills inyectar según el contexto del turno.

    Reglas (en orden de prioridad):
    1. Error reciente en historial  → error-diagnosis + socratic-hint
    2. 3 aciertos consecutivos      → curriculo-matematica + difficulty-calibrator
    3. Estudiante pide la respuesta → socratic-hint
    4. Default                      → curriculo-matematica + socratic-hint
    """
    msg = mensaje.lower()

    pide_respuesta = any(p in msg for p in [
        "cuál es", "cual es", "dime la respuesta", "no sé", "no se",
        "ayúdame", "ayudame", "dime", "cuanto es", "cuánto es", "dame la"
    ])

    aciertos = 0
    for turno in reversed(historial[-5:]):
        if turno.get("resultado") == "correcto":
            aciertos += 1
        elif turno.get("resultado") == "incorrecto":
            return ["error-diagnosis", "socratic-hint"]
        else:
            break

    if aciertos >= 3:
        return ["curriculo-matematica", "difficulty-calibrator"]

    if pide_respuesta:
        return ["socratic-hint"]

    return ["curriculo-matematica", "socratic-hint"]


def _build_system_prompt(skills_activos: list[str], session_state: dict) -> str:
    """Combina los SKILL.md activos + estado de sesión en el system prompt."""
    partes = []

    for skill_name in skills_activos:
        contenido = _load_skill(skill_name)
        partes.append(f"## SKILL ACTIVO: {skill_name.upper()}\n\n{contenido}")

    partes.append(
        "## ESTADO DE SESIÓN\n"
        f"```json\n{json.dumps(session_state, indent=2, ensure_ascii=False)}\n```"
    )

    partes.append(
        "## INSTRUCCIÓN FINAL\n"
        "Eres TutorRD, el tutor de matemáticas del programa EducaT para estudiantes "
        "dominicanos de grados 3 a 9. Responde SIEMPRE en español dominicano accesible "
        "para el grado del estudiante. Sigue estrictamente las reglas del skill activo. "
        "Nunca des la respuesta directa si socratic-hint está activo."
    )

    return "\n\n---\n\n".join(partes)


# ── Capability principal ───────────────────────────────────────────────────────

class TutorRDCapability(BaseCapability):
    manifest = CapabilityManifest(
        name="tutorrd",
        description=(
            "Tutor adaptativo de matemáticas para estudiantes dominicanos. "
            "Pedagogía socrática alineada al currículo MINERD, grados 3–9."
        ),
        stages=["diagnostico", "respuesta_tutor"],
        tools_used=["rag"],
        cli_aliases=["tutor", "tutorrd"],
    )

    async def run(self, context: UnifiedContext, stream: StreamBus) -> None:
        # stream_synthesis es la forma estándar de llamar al LLM en DeepTutor
        from deeptutor.capabilities._answer_now import stream_synthesis

        mensaje = context.user_message or ""
        config  = context.config_overrides or {}

        session_state = {
            "grado":        config.get("grado", 5),
            "tema":         config.get("tema", "matemáticas"),
            "nivel_actual": config.get("nivel_actual", 2),
            "historial":    config.get("historial", []),
        }

        # ── Etapa 1: seleccionar skills y construir system prompt ──────────
        async with stream.stage("diagnostico", source=self.name):
            skills_activos  = _seleccionar_skills(mensaje, session_state["historial"])
            system_prompt   = _build_system_prompt(skills_activos, session_state)

            await stream.progress(
                message=f"Skills activos: {', '.join(skills_activos)}",
                source=self.name,
                stage="diagnostico",
            )

        # ── Etapa 2: llamar al LLM con el system prompt del skill ─────────
        chunks: list[str] = []

        async with stream.stage("respuesta_tutor", source=self.name):
            async for chunk in stream_synthesis(
                stream=stream,
                source=self.name,
                stage="respuesta_tutor",
                trace_meta={},
                system_prompt=system_prompt,
                user_prompt=mensaje,
                max_tokens=1024,
            ):
                chunks.append(chunk)

        respuesta = "".join(chunks)

        await stream.result(
            {
                "response":       respuesta,
                "skills_usados":  skills_activos,
                "session_state":  session_state,
            },
            source=self.name,
        )
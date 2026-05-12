\---

name: tutorrd

description: "Tutor adaptativo de matemáticas para estudiantes dominicanos (EducaT / TutorRD). Pedagogía socrática alineada al currículo MINERD, grados 3–9."

metadata: {"nanobot":{"emoji":"📐","requires":{"bins":\["deeptutor"]}}}

always: false

\---



\# TutorRD — Tutor de Matemáticas Dominicano



Usa el tool `exec` para invocar el tutor adaptativo cuando un estudiante necesite ayuda con matemáticas.



\## Cuándo usar



\- El usuario pide explicación de un concepto matemático (fracciones, multiplicación, ecuaciones, etc.)

\- El usuario está atascado en un ejercicio y no sabe cómo resolverlo

\- El usuario quiere practicar un tema del currículo dominicano (MINERD)

\- El usuario dice "no entiendo", "ayúdame con", "cómo se hace"



\## Comando



```bash

deeptutor run tutorrd "<pregunta o problema del estudiante>" \\

&#x20; --kb minerd-matematica \\

&#x20; --tool rag \\

&#x20; --config grado=5 \\

&#x20; --config tema=fracciones \\

&#x20; --config nivel\_actual=2 \\

&#x20; -l es

```



\## Importante



\- El tutor \*\*nunca da la respuesta directa\*\* — usa pistas socráticas.

\- Si el estudiante no especifica su grado, asume `grado=5`.


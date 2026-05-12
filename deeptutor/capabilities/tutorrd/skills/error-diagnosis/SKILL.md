---
skill: error-diagnosis
version: 1.0
proyecto: EducaT / TutorRD
fase: MVP
---

# Skill: error-diagnosis

## Propósito

Este skill analiza la respuesta incorrecta de un estudiante e identifica **por qué** falló — no solo que falló. Mapea el error a una categoría conceptual del currículo para que el orquestador pueda decidir si se continúa con una pista socrática o si el problema debe ser reformulado desde un concepto previo.

El diagnóstico correcto evita que el tutor repita el mismo ejercicio de otra forma cuando el problema real es una laguna conceptual anterior.

---

## Taxonomía de errores (grados 3–9, matemáticas)

### Categoría 1 — Error de concepto previo
El estudiante no domina un prerrequisito necesario para este problema.

| Error observado | Diagnóstico | Concepto previo a reforzar |
|---|---|---|
| `3 + 4 = 34` | Confusión concatenación vs. suma | Valor de posición / qué es sumar |
| `1/2 + 1/3 = 2/5` | Suma de numeradores y denominadores | Fracciones equivalentes |
| `3 × 0 = 3` | Propiedad del cero no interiorizada | Significado de la multiplicación |
| `-5 + 3 = -8` | Inversión de signo en resta con negativos | Recta numérica / números negativos |

### Categoría 2 — Error de procedimiento
El estudiante entiende el concepto pero aplica mal los pasos.

| Error observado | Diagnóstico |
|---|---|
| Olvida el "llevado" en suma | Error en algoritmo de suma con reagrupación |
| Divide dividendo entre sí mismo | Confusión de roles en la división |
| Resuelve de derecha a izquierda en resta larga | Error en dirección del algoritmo |

### Categoría 3 — Error de lectura del problema
El estudiante malinterpretó lo que se pedía, no tiene déficit matemático.

| Señal | Diagnóstico |
|---|---|
| Suma cuando se pide diferencia | No identificó la operación requerida |
| Da resultado parcial como respuesta final | No identificó que había múltiples pasos |
| Responde con unidad incorrecta (metros en vez de cm) | No leyó las unidades del enunciado |

### Categoría 4 — Error de atención / transcripción
El razonamiento es correcto pero el estudiante escribió algo diferente a lo que calculó.

Señal: el proceso intermedio visible es correcto pero la respuesta final difiere por un dígito o signo.

---

## Protocolo de diagnóstico

Al recibir una respuesta incorrecta, el tutor debe:

1. **Identificar la categoría** del error usando la taxonomía anterior.
2. **No revelar el diagnóstico** al estudiante directamente — usarlo internamente para elegir la respuesta correcta.
3. **Actuar según categoría:**

| Categoría | Acción del tutor |
|---|---|
| 1 — Concepto previo | Retroceder al concepto base. Reformular desde ese punto. No continuar con el ejercicio actual hasta cerrar la laguna. |
| 2 — Procedimiento | Pedir al estudiante que muestre su proceso paso a paso. Identificar en qué paso se desvió. |
| 3 — Lectura | Leer el enunciado juntos. Preguntar "¿qué te está pidiendo este problema?" antes de resolver. |
| 4 — Atención | Pedir al estudiante que revise su respuesta: "¿Estás seguro de ese número? Revisa tu proceso." |

---

## Output esperado del skill

Cuando este skill está activo, el tutor produce internamente una etiqueta de diagnóstico antes de responder:

```
[DIAGNÓSTICO: Categoría 1 — suma de fracciones sin denominador común]
[ACCIÓN: Retroceder a fracciones equivalentes antes de continuar]
```

Esta etiqueta **no se muestra al estudiante**. Se usa para construir la respuesta apropiada.

---

## Ejemplo completo

**Problema dado:** ¿Cuánto es 1/4 + 1/2?

**Respuesta del estudiante:** *"2/6"*

**Diagnóstico interno:**
```
[DIAGNÓSTICO: Categoría 1 — sumó numeradores (1+1=2) y denominadores (4+2=6)]
[CONCEPTO PREVIO FALTANTE: Fracciones equivalentes / denominador común]
[ACCIÓN: No continuar con suma. Preguntar qué fracción equivale a 1/2 con denominador 4]
```

**Respuesta del tutor:**
*"Interesante. Antes de sumar, dime: ¿Puedes escribir 1/2 de otra forma, pero usando el número 4 abajo? Piénsalo como: ¿cuántas partes de 4 son lo mismo que una mitad?"*

---

## Integración con otros skills

- Alimenta a `socratic-hint`: le indica qué tipo de pista generar.
- Alimenta a `difficulty-calibrator`: si hay error de categoría 1 repetido, el calibrador debe bajar el nivel.
- Alimenta al `session-summarizer` (fase 3): registra qué conceptos presentaron dificultad en la sesión.

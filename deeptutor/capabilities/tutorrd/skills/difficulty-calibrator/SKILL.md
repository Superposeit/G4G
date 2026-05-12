---
skill: difficulty-calibrator
version: 1.0
proyecto: EducaT / TutorRD
fase: MVP
---

# Skill: difficulty-calibrator

## Propósito

Este skill observa el historial de respuestas del estudiante en la sesión actual y decide cuándo y cómo ajustar la dificultad del siguiente ejercicio. Su objetivo es mantener al estudiante en su Zona de Desarrollo Próximo: suficientemente desafiado para aprender, nunca tan frustrado como para abandonar.

---

## Estado de sesión requerido

Este skill necesita acceso al historial de la sesión. El orquestador Python debe proveer este contexto en cada llamada:

```json
{
  "grado": 5,
  "tema_actual": "multiplicación",
  "historial": [
    {"ejercicio": "3×4", "resultado": "correcto", "tiempo_seg": 12},
    {"ejercicio": "6×7", "resultado": "correcto", "tiempo_seg": 9},
    {"ejercicio": "8×9", "resultado": "correcto", "tiempo_seg": 8}
  ],
  "nivel_actual": 2
}
```

---

## Escala de dificultad

Cada tema tiene 5 niveles. El estudiante comienza en el nivel 2 (no en el 1) para evitar condescendencia.

### Ejemplo para multiplicación (grado 5):

| Nivel | Descripción | Ejemplo |
|---|---|---|
| 1 | Tablas del 1–5, números pequeños | 2×3, 4×2 |
| 2 | Tablas del 1–10 | 7×6, 9×3 |
| 3 | Un dígito × dos dígitos | 8×13, 6×24 |
| 4 | Dos dígitos × dos dígitos | 23×14, 45×32 |
| 5 | Problemas de contexto, múltiples pasos | "Si una caja tiene 24 mangos y compro 12 cajas, ¿cuántos mangos tengo?" |

---

## Reglas de ajuste

### Subir un nivel (nivel + 1)
**Condición:** 3 respuestas correctas consecutivas Y tiempo de respuesta decreciente (el estudiante acelera).

**Acción:** Generar el siguiente ejercicio en nivel + 1.

**Mensaje al estudiante:**
*"Muy bien, eso ya lo tienes dominado. Vamos con algo un poco más interesante."*

---

### Mantener el nivel actual
**Condición:** Mezcla de aciertos y errores, sin patrón claro. O el estudiante acertó pero tomó tiempo largo (correcto pero con esfuerzo visible).

**Acción:** Generar otro ejercicio del mismo nivel, pero con números diferentes.

**Sin mensaje especial** — continuar fluidamente.

---

### Bajar un nivel (nivel - 1)
**Condición A:** 2 errores consecutivos en el mismo nivel.
**Condición B:** `error-diagnosis` reporta un error de Categoría 1 (laguna conceptual).

**Acción:** Bajar al nivel anterior y reformular con un ejemplo de contexto dominicano para reactivar el concepto.

**Mensaje al estudiante:**
*"Vamos a practicar un poco más este paso. Te pongo uno más directo para arrancar."*

---

### Pausa pedagógica (nivel 1 con errores repetidos)
**Condición:** El estudiante está en nivel 1 y sigue fallando en el mismo concepto (3+ errores).

**Acción:** No seguir generando ejercicios. Activar una explicación conceptual breve antes de continuar.

**Mensaje al estudiante:**
*"Antes de seguir con ejercicios, déjame explicarte algo sobre [concepto]. Solo un momento."*

---

## Lógica de generación del siguiente ejercicio

Al generar un nuevo ejercicio, el skill debe:

1. Respetar el nivel calculado.
2. Cambiar los números del ejercicio anterior (nunca repetir el mismo).
3. Si el nivel subió, aumentar la complejidad gradualmente — no saltar dos niveles de golpe.
4. Cada 2–3 ejercicios de nivel ≥ 3, incluir al menos uno con contexto dominicano (problema de texto).

### Banco de contextos dominicanos para problemas
- Compras en el colmado / mercado
- Transporte: guaguas, carros de concho
- Agricultura: cosechas, siembra
- Playa / pesca: turistas, libras de pescado
- Escuela: cuadernos, lápices, estudiantes por aula

---

## Ejemplo de flujo completo

**Historial:**
- Ejercicio 1 (nivel 2): 6×7 → correcto, 14 seg
- Ejercicio 2 (nivel 2): 8×4 → correcto, 10 seg
- Ejercicio 3 (nivel 2): 9×6 → correcto, 9 seg

**Decisión del calibrador:**
```
[CALIBRADOR: 3 aciertos consecutivos, tiempo decreciente]
[DECISIÓN: Subir a nivel 3]
[PRÓXIMO EJERCICIO: 7 × 13]
```

**Mensaje:** *"Muy bien, eso ya lo tienes dominado. Vamos con algo un poco más interesante."*

**Ejercicio generado:** *"¿Cuánto es 7 × 13?"*

---

## Límites del skill

- **No sube más de 1 nivel por turno**, aunque el estudiante tenga una racha larga.
- **No baja más de 1 nivel por turno**, aunque el error sea severo (el `error-diagnosis` maneja la profundidad).
- **No evalúa velocidad sola** — un estudiante lento pero correcto no baja de nivel.
- El nivel **no baja por debajo de 1** ni sube **por encima de 5**.

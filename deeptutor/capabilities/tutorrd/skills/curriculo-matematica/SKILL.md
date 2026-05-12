---
skill: curriculo-matematica
version: 1.0
proyecto: EducaT / TutorRD
fase: MVP
nota: Incluye contexto cultural RD (skill fusionado)
---

# Skill: curriculo-matematica

## Propósito

Este skill define **qué enseña** el tutor. Contiene la estructura del currículo de matemáticas del Ministerio de Educación de la República Dominicana (MINERD) para grados 3–9, la secuencia de conceptos por grado, y ejemplos contextualizados en la cultura y realidad dominicana. Es la "memoria curricular" del tutor.

> **Nota de fusión:** Este skill incluye las responsabilidades de `contexto-cultural-rd`. Todos los ejemplos y ejercicios generados por el tutor deben estar anclados en situaciones recognocibles para el estudiante dominicano — rural o urbano.

---

## Estructura curricular por bloque de grados

### Bloque A — Grados 3, 4 y 5

#### Grado 3
| Tema | Conceptos clave |
|---|---|
| Números naturales | Lectura y escritura hasta 9,999. Orden y comparación. |
| Suma y resta | Algoritmos con reagrupación. Estimación. |
| Multiplicación | Concepto como suma repetida. Tablas del 1 al 5. |
| Geometría básica | Figuras planas: cuadrado, triángulo, círculo, rectángulo. |
| Medición | Unidades de longitud (cm, m). Tiempo (horas, días). |

#### Grado 4
| Tema | Conceptos clave |
|---|---|
| Números naturales | Hasta 999,999. Valor posicional. |
| Multiplicación | Tablas del 1 al 10. Un dígito × dos dígitos. |
| División | Concepto, cociente, residuo. División exacta e inexacta. |
| Fracciones | Concepto de fracción. Fracciones propias e impropias. |
| Geometría | Perímetro de figuras planas. |
| Estadística básica | Lectura de tablas y pictogramas. |

#### Grado 5
| Tema | Conceptos clave |
|---|---|
| Operaciones | Dos dígitos × dos dígitos. División con dos dígitos. |
| Fracciones | Fracciones equivalentes. Suma y resta con mismo denominador. |
| Números decimales | Décimas y centésimas. Lectura y escritura. |
| Geometría | Área de rectángulo y cuadrado. |
| Medición | Unidades de masa (kg, g). Capacidad (litros, ml). |

---

### Bloque B — Grados 6, 7, 8 y 9

#### Grado 6
| Tema | Conceptos clave |
|---|---|
| Fracciones | Suma y resta con diferente denominador. MCM. |
| Decimales | Operaciones con decimales. Redondeo. |
| Porcentajes | Concepto. Cálculo del % de una cantidad. |
| Razones y proporciones | Razón simple. Proporción directa. |
| Geometría | Triángulos: clasificación y ángulos. |

#### Grado 7
| Tema | Conceptos clave |
|---|---|
| Números enteros | Negativos. Recta numérica. Operaciones. |
| Álgebra introductoria | Expresiones algebraicas. Valor numérico. |
| Ecuaciones | Ecuaciones de primer grado con una incógnita. |
| Geometría | Cuadriláteros. Ángulos en polígonos. |
| Estadística | Media, mediana, moda. |

#### Grado 8
| Tema | Conceptos clave |
|---|---|
| Álgebra | Productos notables. Factorización básica. |
| Sistemas de ecuaciones | Dos ecuaciones, dos incógnitas. Método de sustitución. |
| Geometría | Teorema de Pitágoras. Círculo: área y circunferencia. |
| Funciones | Concepto de función. Tabla de valores. Gráfica. |

#### Grado 9
| Tema | Conceptos clave |
|---|---|
| Funciones | Función lineal y cuadrática. |
| Geometría analítica | Plano cartesiano. Pendiente. Ecuación de recta. |
| Trigonometría básica | Razones trigonométricas en triángulo rectángulo. |
| Estadística | Frecuencias. Histogramas. Medidas de dispersión. |

---

## Secuencia de prerequisitos (mapa de dependencias)

Antes de abordar un tema, el tutor debe verificar que el estudiante domina sus prerequisitos:

```
Suma y resta (G3)
    └── Multiplicación tablas (G3-G4)
            └── Multiplicación 2 dígitos (G5)
                    └── División (G4-G5)
                            └── Fracciones concepto (G4)
                                    └── Fracciones equivalentes (G5)
                                            └── Suma fracciones distinto denominador (G6)
                                                    └── Porcentajes (G6)

Números naturales (G3-G4)
    └── Decimales (G5)
            └── Operaciones con decimales (G6)

División (G5)
    └── Números negativos (G7)
            └── Ecuaciones (G7)
                    └── Sistemas de ecuaciones (G8)
```

---

## Banco de contextos culturales dominicanos

El tutor debe priorizar estos contextos al generar ejemplos y problemas. Esto hace el contenido inmediatamente recognocible para el estudiante.

### Contextos rurales
- **Agricultura:** Cosecha de plátanos, yuca, café, cacao. Tamaño de parcelas en tareas de tierra.
- **Ganadería:** Número de reses, litros de leche por vaca, peso en libras.
- **Batey / campo:** Distancias en caminos de tierra, grupos de familias.

### Contextos urbanos / semiurbanos
- **Colmado:** Compras cotidianas, cambio de dinero, precios en pesos.
- **Mercado:** Peso de frutas (mangos, guineos, chinas), costo por libra.
- **Transporte:** Carros de concho (precio por pasajero), guaguas (capacidad, rutas).
- **Escuela:** Estudiantes por aula, cuadernos, lápices, uniformes.

### Contextos generales dominicanos
- **Playa / turismo:** Turistas, habitaciones de hotel, libras de pescado.
- **Béisbol:** Estadísticas de jugadores dominicanos, innings, carreras.
- **Fiestas patrias / carnaval:** Grupos de personas, trajes, dinero recaudado.

---

## Ejemplos contextualizados por tema

### Multiplicación (Grado 5)
❌ Genérico: *"Juan tiene 5 manzanas y compra 3 cajas de 5."*
✅ Contextualizado: *"Doña Carmen vende guineos en el mercado. Cada racimo tiene 8 guineos. Si vendió 7 racimos hoy, ¿cuántos guineos vendió en total?"*

### Fracciones (Grado 6)
❌ Genérico: *"Una pizza dividida en 4 partes."*
✅ Contextualizado: *"Un conuco tiene 3/4 de tarea sembrada de yuca y 1/2 tarea sembrada de plátano. ¿Cuánto del conuco está sembrado en total?"*

### Porcentajes (Grado 6)
❌ Genérico: *"Un descuento del 20% en una tienda."*
✅ Contextualizado: *"En las rebajas del Día de la Altagracia, una mochila cuesta 850 pesos. Si tiene un 20% de descuento, ¿cuánto pagas?"*

### Ecuaciones (Grado 7)
❌ Genérico: *"x + 5 = 12"*
✅ Contextualizado: *"Un carro de concho cobra la misma tarifa a cada pasajero. Si llevó 4 pasajeros y cobró 200 pesos en total, ¿cuánto cobró por persona?"*

---

## Instrucciones de uso para el tutor

1. Al recibir el grado del estudiante y el tema de la sesión, consultar la tabla correspondiente para saber qué conceptos son relevantes.
2. Antes de introducir un tema nuevo, verificar los prerequisitos en el mapa de dependencias.
3. Al generar cualquier ejemplo o ejercicio, seleccionar un contexto del banco cultural dominicano.
4. No introducir vocabulario matemático no incluido en el nivel del estudiante.
5. Si el estudiante pregunta por un tema fuera del bloque de su grado, responder con calidez y redirigir: *"Ese tema lo vas a ver más adelante. Por ahora practiquemos [tema actual]."*

---

## Idioma y registro lingüístico

- **Idioma:** Español dominicano accesible. Nunca español peninsular.
- **Evitar:** *"vosotros"*, *"ordenador"*, *"carnet"*, *"guay"* — usar *"ustedes"*, *"computadora"*, *"carné"*, *"chévere"*.
- **Registro:** Conversacional, sin tecnicismos fuera del nivel. Una oración por idea.
- **Moneda:** Pesos dominicanos (RD$), no dólares, salvo en problemas de grado 8–9 donde la conversión sea el tema.

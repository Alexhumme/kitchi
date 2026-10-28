# ADR-003 — Estrategia de integración de IA

- **Estado:** Propuesto — **pendiente de decisión** tras la prueba comparativa de los días 1–3 (tarea P05)
- **Fecha:** 2026-10-26
- **Responsables:** Integrante C (decisión), todo el equipo (validación con la rúbrica del profesor)

## Contexto y problema

El MVP debe incluir una integración de IA real y demostrable (AC-08) que transforme fotografías de personas o gatos reales en representaciones felinas estilizadas, con presupuesto cero, sin GPU garantizada y con un plazo de cuatro semanas. El PDF del curso permite usar IA, pero no la exige: la integración es un diferenciador de producto y no puede bloquear las tres funcionalidades mínimas. La decisión sobre el modelo sigue pendiente de la prueba comparativa de los días 28–31 de octubre (tarea P05).

## Alternativas evaluadas

Detalle completo en [07_AI_INTEGRATION.md](../07_AI_INTEGRATION.md):

| Alternativa | Ventaja principal | Riesgo principal |
| --- | --- | --- |
| **A — Servicio generativo externo** | Menos infraestructura local | Límites gratuitos, claves API, privacidad, consistencia |
| **B — Modelo preentrenado local** | Control del entorno, sin coste por petición | GPU, memoria, instalación, tiempo de inferencia |
| **C — IA asistida por catálogo** | Resultados consistentes, menor dependencia gráfica | Parecido limitado con la fotografía |

## Decisión

**(Pendiente)** Diseñar la arquitectura para admitir las tres alternativas (adaptador de proveedor en el motor de generación) e implementar inicialmente una sola. Recomendación del plan maestro: si no hay GPU ni API gratuita confirmada, **C es la más segura para terminar a tiempo**, pero para cumplir con rigor debe existir inferencia real de un modelo, no una selección aleatoria de opciones.

Completa el criterio de selección del documento [07_AI_INTEGRATION.md](../07_AI_INTEGRATION.md) con las 7 preguntas de la prueba comparativa y sus respuestas antes de marcar este ADR como Aceptado.

## Justificación

- La IA no puede bloquear el flujo principal: el editor manual y la generación de stickers funcionan sin ella (contingencia).
- El adaptador permite cambiar de proveedor o modo sin reescribir el subsistema.

## Consecuencias y riesgos

- **Riesgo alto / probabilidad alta:** IA gratuita no disponible o limitada → validación en semana 1 y adaptador de proveedor.
- Si la prueba consume más tiempo del presupuestado, se congela el alcance de IA y se documenta (regla de retrasos de [01_MASTER_PLAN.md](../01_MASTER_PLAN.md)).
- Si la rúbrica del docente cambia y exige IA central, y no hay alternativa viable sin coste, la prueba de concepto de la semana 1 es puerta de decisión: renegociar alcance con el profesor. Con la rúbrica vigente, la IA es un diferenciador y no bloquea la entrega.
- Privacidad: registrar en este ADR si el servicio externo recibe fotografías y con qué consentimiento.

## Plantilla de cierre (rellenar tras la prueba)

```
Modelo/servicio elegido:
Fecha de prueba:
Resultado de las 7 preguntas:
GPU disponible: sí / no
Coste: 0 / otro
Decisión final: A / B / C / contingencia documentada
Firmas:
```

# ADR-004 — Adecuación del proyecto a la rúbrica del curso

- **Estado:** Aceptado
- **Fecha:** 2026-10-28
- **Responsables:** Todo el equipo

## Contexto y problema

El profesor publicó el documento [`Proyecto-final-Programacion-Avanzada-A1-20262.pdf`](../Proyecto-final-Programacion-Avanzada-A1-20262.pdf) con la rúbrica, los entregables y la fecha límite del proyecto final. La documentación previa asumía cinco semanas, no incluía las secciones obligatorias del README, no tenía un plan explícito de commits por integrante y trataba la concurrencia, el multiprocesamiento y el paralelismo como requisitos académicos centrales, cuando el PDF no los exige explícitamente.

Además, la rúbrica evalúa la sustentación individual y la capacidad de cada integrante de explicar cualquier parte del código. El equipo necesitaba un documento de estudio que se construyera por incrementos y no al final.

## Alternativas evaluadas

1. **Mantener el plan de cinco semanas y ajustar al final** — descartada: la fecha límite es el 25 de noviembre de 2026 y no admite entregas tardías.
2. **Cambiar de stack a una aplicación monolítica Django** — descartada: Flet + Django REST Framework cumple el requisito de interfaz real y API, y ya está documentado en [ADR-001](ADR-001-frontend-backend.md). El PDF no impone un stack concreto.
3. **Retirar la IA y la programación avanzada para reducir alcance** — descartada: son diferenciadores de alcance y calidad técnica; se mantienen, pero subordinados a las tres funcionalidades mínimas.
4. **Alinear la documentación y el calendario a la rúbrica, conservando la arquitectura** (elegida).

## Decisión

1. La rúbrica del PDF es la fuente vigente para el alcance, los entregables y el calendario.
2. El proyecto se planifica en **cuatro semanas** (28 de octubre – 25 de noviembre de 2026), con entrega interna el 24 de noviembre.
3. Se mantiene **Flet Web + Django REST Framework + MySQL + Pillow**, porque cumple el requisito de aplicación real con interfaz, API, base de datos y documentación automática.
4. Se añade **drf-spectacular** para Swagger/OpenAPI en `/api/schema/` y `/api/docs/`.
5. El **README** se convierte en entregable de primera clase: nombre, problema, instalación/ejecución, uso de IA, integrantes y enlace al repositorio.
6. Se establece una **política de commits**: mínimo 5 commits descriptivos por integrante, incluida la diseñadora; repositorio público y sin secretos.
7. La **sustentación** se diseña para 10 minutos: 6–7 minutos de demo y 3–4 de preguntas individuales.
8. Se crea [`12_GUIA_PLATAFORMA.md`](../12_GUIA_PLATAFORMA.md) como guía viva, casi vacía al inicio y actualizada en cada incremento, para la preparación individual.
9. La **concurrencia, el multiprocesamiento y el paralelismo** se conservan como diferenciadores de calidad técnica, no como requisito explícito del PDF. No deben comprometer las tres funcionalidades mínimas.
10. La **IA del producto** se conserva como diferenciador. El flujo manual y la contingencia siguen siendo obligatorios.

## Justificación

- El calendario de cuatro semanas es el único compatible con la fecha límite.
- El stack existente ya satisface los requisitos del PDF y evitar cambiarlo reduce el riesgo técnico.
- Swagger/OpenAPI y un README completo son evidencia directa para los criterios 3 y 5.
- La guía viva y los ensayos individuales atacan el criterio 4, que puede bajar la nota de una persona aunque el producto funcione.
- Mantener la IA y el benchmark como diferenciadores permite aspirar a un alcance sobresaliente sin convertirlos en puertas de entrega.

## Consecuencias y riesgos

- **Obligatorio:** actualizar [`README.md`](../../README.md) con nombres e instrucciones verificadas antes de la entrega.
- **Obligatorio:** crear `requirements.txt` o `pyproject.toml` con versiones fijadas y validar la instalación desde un clon limpio.
- **Obligatorio:** cada integrante debe acumular commits propios y participar en los ensayos.
- **Riesgo:** MySQL puede dificultar un clon limpio. Se valida en P29; si bloquea la demo, se registrará un ADR de contingencia (SQLite) sin cambiar el modelo de datos.
- **Riesgo:** la IA puede consumir tiempo. Si no hay una inferencia real viable, se documenta la contingencia y se prioriza el resto del producto.
- **Riesgo:** la guía viva se puede dejar para el final. La regla de actualización por incremento en [`AGENTS.md`](../../AGENTS.md) lo impide.

## Documentos afectados

[`AGENTS.md`](../../AGENTS.md) · [`README.md`](../../README.md) · [`00_PROJECT_OVERVIEW.md`](../00_PROJECT_OVERVIEW.md) · [`01_MASTER_PLAN.md`](../01_MASTER_PLAN.md) · [`02_REQUIREMENTS.md`](../02_REQUIREMENTS.md) · [`03_ARCHITECTURE.md`](../03_ARCHITECTURE.md) · [`05_API_CONTRACTS.md`](../05_API_CONTRACTS.md) · [`09_TEST_PLAN.md`](../09_TEST_PLAN.md) · [`10_DEVELOPMENT_CHECKLIST.md`](../10_DEVELOPMENT_CHECKLIST.md) · [`11_DEMO_SCRIPT.md`](../11_DEMO_SCRIPT.md) · [`12_GUIA_PLATAFORMA.md`](../12_GUIA_PLATAFORMA.md) · [`13_CUMPLIMIENTO_ACADEMICO.md`](../13_CUMPLIMIENTO_ACADEMICO.md)

# Reportes y evidencias — Kitchi Studio

Directorio de evidencias reproducibles exigidas por el plan maestro. Cada archivo debe permitir que un evaluador entienda **qué** se midió, **cómo** y **con qué resultado**, sin reconstruir el contexto.

## Contenidos previstos

| Archivo | Contenido | Criterio relacionado | Tarea |
| --- | --- | --- | --- |
| `rubric.md` | Rúbrica transcrita del profesor y respuestas a las preguntas de [01_MASTER_PLAN.md](../01_MASTER_PLAN.md) | AC-09…AC-11 (adaptación) | P01 |
| `week1-validation.md` | Validación de Flet, DRF, MySQL y Pillow (versiones exactas fijadas) | AC-12 | P02 |
| `ai-evaluation.md` | Prueba comparativa de IA: las 7 preguntas de [07_AI_INTEGRATION.md](../../07_AI_INTEGRATION.md) | AC-08 | P05 |
| `concurrency-logs.md` | Logs de la prueba concurrente con operaciones reales | AC-09 | P20 |
| `multiprocessing-evidence.md` | Identificación de procesos trabajadores y resultados | AC-10 | P21 |
| `benchmark.md` | Benchmark secuencial vs paralelo: equipo, versión de Python, tamaño de imágenes, repeticiones, metodología y aceleración | AC-11 | P22, P27 |
| `acceptance-run.md` | Recorrido del escenario de aceptación principal (9 pasos) | AC-01…AC-07, AC-12–AC-14 | P24 |
| `clean-install.md` | Registro de instalación y ejecución desde un clon limpio | AC-13 | P29 |

## Reglas

- Incluir siempre fecha, versión del código (commit o etiqueta) y entorno utilizado.
- No presentar mediciones como garantías de rendimiento en producción.
- No inventar cifras: si una prueba no se ejecutó, decirlo explícitamente.
- Las capturas y salidas crudas pueden guardarse junto al informe o en `storage/` si son voluminosas (fuera de Git).

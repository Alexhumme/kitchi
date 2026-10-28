# Reportes y evidencias — Kitchi Studio

Directorio de evidencias reproducibles exigidas por el plan maestro y por la rúbrica del curso. Cada archivo debe permitir que un evaluador entienda **qué** se midió, **cómo** y **con qué resultado**, sin reconstruir el contexto.

## Contenidos

| Archivo | Contenido | Criterio relacionado | Tarea |
| --- | --- | --- | --- |
| [`rubric.md`](rubric.md) | Rúbrica del PDF transcrita y sus implicaciones para el proyecto | Criterios 1–5 | P01 |
| `academic-audit.md` | Auditoría final de README, repositorio, producto y sustentación | Criterios 2, 3 y 5 | P40 |
| `week1-validation.md` | Validación de Flet, DRF, MySQL, Pillow y Swagger (versiones exactas fijadas) | Criterio 2 / AC-12 | P02 |
| `ai-evaluation.md` | Prueba comparativa de IA: las 7 preguntas de [07_AI_INTEGRATION.md](../07_AI_INTEGRATION.md) | AC-08 | P05 |
| `concurrency-logs.md` | Logs de la prueba concurrente con operaciones reales | AC-09 | P20 |
| `multiprocessing-evidence.md` | Identificación de procesos trabajadores y resultados | AC-10 | P21 |
| `benchmark.md` | Benchmark secuencial vs paralelo: equipo, versión de Python, tamaño de imágenes, repeticiones, metodología y aceleración | AC-11 | P22, P27 |
| `acceptance-run.md` | Recorrido del escenario de aceptación principal (9 pasos) | AC-01…AC-07, AC-12–AC-14 | P24 |
| `clean-install.md` | Registro de instalación y ejecución desde un clon limpio | AC-13 / criterio 5 | P29 |
| `readme-check.md` | Verificación de las secciones obligatorias del README | Criterio 5 | P31 |
| `commits-audit.md` | Conteo de commits por integrante y revisión de secretos | Criterio 5 | P34 |
| `defense-rehearsal.md` | Registro de ensayos de la defensa de 10 minutos y preguntas individuales | Criterio 4 | P37 |

> Los archivos que aún no existen se crean al ejecutar la tarea correspondiente. No se inventan resultados.

## Reglas

- Incluir siempre fecha, versión del código (commit o etiqueta) y entorno utilizado.
- No presentar mediciones como garantías de rendimiento en producción.
- No inventar cifras: si una prueba no se ejecutó, decirlo explícitamente.
- Las capturas y salidas crudas pueden guardarse junto al informe o en `storage/` si son voluminosas (fuera de Git).
- No incluir secretos, tokens, rutas personales ni fotografías privadas en las evidencias.
- La auditoría final debe coincidir con [`13_CUMPLIMIENTO_ACADEMICO.md`](../13_CUMPLIMIENTO_ACADEMICO.md).

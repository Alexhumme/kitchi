# Reportes y evidencias — Kitchi Studio

Directorio de evidencias reproducibles exigidas por el plan maestro y por la rúbrica del curso. Cada archivo debe permitir que un evaluador entienda **qué** se midió, **cómo** y **con qué resultado**, sin reconstruir el contexto.

## Contenidos

| Archivo | Contenido | Criterio relacionado | Tarea |
| --- | --- | --- | --- |
| [`rubric.md`](rubric.md) | Rúbrica del PDF transcrita y sus implicaciones para el proyecto | Criterios 1–5 | P01 |
| `academic-audit.md` | Auditoría final de README, repositorio, producto y sustentación | Criterios 2, 3 y 5 | P40 |
| `week1-validation.md` | Validación histórica de Flet, DRF, MySQL, Pillow y Swagger (versiones exactas fijadas) | Criterio 2 / AC-12 | P02 |
| [`frontend-integration.md`](frontend-integration.md) | Evidencia histórica de integración Flet ↔ API, catálogo provisional, 34 pruebas y smoke test de pantallas | Criterio 2 / AC-12 | P02, P08, P10, P12, P36, P39 |
| [`frontend-flet-web-startup.md`](frontend-flet-web-startup.md) | Evidencia histórica del arranque Flet y del recorrido por sus cinco secciones | Criterio 2 / AC-12 | P10, P12, P36, P39 |
| [`frontend-react.md`](frontend-react.md) | Historia y estado actual de React como única interfaz activa, con verificación de build, lint y flujo contra MySQL | Criterio 2 / AC-12 | P02, P10, P12, P36 |
| [`editor-visual-assets.md`](editor-visual-assets.md) | Editor SVG real, cabeza delantera, orden de capas, colores, multiaccesorio, MySQL y capturas | Criterio 2 / AC-01, AC-02, AC-06 | P06, P08, P09, P10, P12, P36 |
| [`p18-hub-publicaciones.md`](p18-hub-publicaciones.md) | Hub de publicaciones extremo a extremo: publicación autenticada, feed público, perfiles públicos y estilo juguetón global | Criterio 2 / AC-07 (primera parte) | P18 |
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

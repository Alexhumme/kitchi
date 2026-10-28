# 07 · Integración de IA — Kitchi Studio

Alternativas, flujo, seguridad, contingencia y uso de IA en el desarrollo · Versión 1.1 · 28 de octubre de 2026

> La IA se integra como un **subsistema independiente**. No debe convertirse en un requisito para abrir el editor, personalizar un gato o generar stickers desde recursos 2D ([ADR-003](decisions/ADR-003-ai-strategy.md)).

> **Alcance académico:** el PDF del curso permite usar IA para desarrollar y dentro de la aplicación, pero **no la exige**. En Kitchi Studio se conserva como diferenciador de producto. Si la inferencia real no es viable, se documenta la contingencia y se priorizan las tres funcionalidades mínimas de [`02_REQUIREMENTS.md`](02_REQUIREMENTS.md).

Hay una diferencia importante entre crear un personaje original y transformar una fotografía de una persona o mascota en una representación felina. El segundo caso es más difícil: exige preservar rasgos reconocibles, controlar el estilo y obtener resultados utilizables como piezas gráficas.

## Alternativas a evaluar

### Alternativa A — Modelo generativo mediante servicio externo

Se envía una imagen de referencia y una instrucción para obtener un gato chibi. El resultado se muestra al usuario y puede servir como referencia para personalizar el personaje.

- Ventajas: menos infraestructura local.
- Riesgos: límites gratuitos variables, claves API, disponibilidad, privacidad y consistencia entre resultados.

### Alternativa B — Modelo preentrenado local

El grupo ejecuta un modelo generativo ya entrenado y lo invoca desde Python.

- Ventajas: mayor control del entorno y sin cobro por petición a un proveedor.
- Riesgos: requisitos de GPU, memoria, instalación, tiempo de inferencia y calidad variable.

### Alternativa C — IA asistida por catálogo

La IA propone atributos o variantes de un gato y el motor 2D compone la imagen con recursos de la marca.

- Ventajas: resultados visualmente consistentes y menor dependencia de generación gráfica completa.
- Riesgos: el parecido con la fotografía será limitado.

### Recomendación para el MVP

Diseñar una arquitectura que admita las tres alternativas, pero implementar inicialmente **una sola**. Si el equipo no dispone de GPU ni de una API gratuita confirmada, la alternativa C es la más segura para terminar a tiempo, aunque no satisface por sí sola una transformación fotorrealista o de gran parecido.

> Para cumplir el requisito de IA con rigor, deberá existir una **inferencia real de un modelo**, no solo una selección aleatoria de opciones (AC-08 en [02_REQUIREMENTS.md](02_REQUIREMENTS.md)).

## Flujo propuesto

```
Usuario selecciona foto
        ▼
Validar formato y tamaño
        ▼
¿Archivo válido? ── No ──► Mostrar error
        │ Sí
        ▼
Crear trabajo de IA (generation_jobs)
        ▼
Ejecutar modelo
        ▼
¿Resultado válido? ── No ──► Registrar fallo y permitir reintento
        │ Sí
        ▼
Guardar resultado temporal
        ▼
Mostrar previsualización
        ▼
¿Usuario acepta el resultado? ── No ──► Reintentar / abandonar
        │ Sí
        ▼
Crear configuración editable
        ▼
Continuar en el editor 2D
```

El modelo puede generar una **imagen de referencia** que el usuario acepte y luego utilice como guía para seleccionar rasgos manualmente. **No se debe prometer** que una imagen generada se convertirá automáticamente en capas editables: esa transformación exige segmentación y reconstrucción adicionales, fuera del MVP.

## Uso de IA en el desarrollo del proyecto

La rúbrica permite asistentes de IA, pero exige que cada integrante pueda explicar cualquier parte del código y que el README declare qué herramientas se usaron y en qué partes. Reglas:

- El README incluye una sección **“Uso de IA”** con herramientas, propósito y módulos afectados.
- Cada integrante declara las herramientas que usó en su trabajo.
- Ningún integrante presenta código generado por IA que no pueda explicar, modificar o depurar.
- La IA para desarrollar (asistentes, autocompletado, revisión) se documenta por separado de la IA del producto (inferencia sobre fotografías).
- No se pegan claves, tokens, fotografías privadas ni datos de usuarios en herramientas externas.
- Las respuestas de la IA se revisan y se prueban; no se aceptan como evidencia de que una función funciona.

Plantilla para el README:

```markdown
## Uso de IA

| Herramienta | Para qué se usó | Partes del proyecto |
| --- | --- | --- |
| OpenCode (agente de IA) | Análisis de la rúbrica, redacción y revisión de documentación | docs/, README, AGENTS |
| ... | ... | ... |
```

## Requisitos de seguridad y privacidad

- Aceptar únicamente formatos de imagen permitidos.
- Limitar el tamaño de los archivos subidos.
- No almacenar fotografías originales más tiempo del necesario.
- Evitar guardar imágenes en directorios públicos.
- No registrar imágenes, tokens o datos sensibles en los logs.
- Eliminar archivos temporales tras el procesamiento o la expiración definida.
- Documentar si el servicio externo recibe fotografías.
- Obtener consentimiento para el procesamiento de imágenes.
- Si se admiten fotografías de menores, no recopilar ni publicar esas imágenes sin una política específica y medidas de protección adecuadas.

**La clave de cualquier proveedor de IA debe permanecer en el backend o en variables de entorno locales, nunca en el código de la interfaz ni en el repositorio.** (Ver [`.env.example`](../.env.example); riesgo cubierto por AC-14.)

## Criterio para elegir el modelo

Durante los primeros tres días (28–31 de octubre), realizar una prueba comparativa breve y documentar las respuestas en [`reports/ai-evaluation.md`](reports/ai-evaluation.md):

1. ¿Se puede ejecutar sin coste?
2. ¿Acepta imágenes como entrada?
3. ¿Produce un gato ilustrado reconocible?
4. ¿Se puede utilizar legalmente bajo sus condiciones?
5. ¿Cuál es el tiempo de inferencia?
6. ¿Qué ocurre cuando falla?
7. ¿Puede ejecutarse en los equipos disponibles?

La decisión se registra en [`decisions/ADR-003-ai-strategy.md`](decisions/ADR-003-ai-strategy.md). Si la prueba de IA consume más tiempo del presupuestado, **se congela el alcance de esta función** y se continúa con el editor manual (regla de retrasos de [01_MASTER_PLAN.md](01_MASTER_PLAN.md)).

## Plan de contingencia

La arquitectura debe permitir desactivar la integración de IA sin desactivar el resto de la aplicación. El modo de contingencia tiene estas propiedades:

- El editor manual sigue funcionando.
- El motor de composición sigue generando los seis stickers.
- Los errores de IA se muestran como estados comprensibles.
- La aplicación **no finge** que una inferencia se ejecutó si no ocurrió.
- La demostración distingue claramente entre funcionalidades reales y simuladas.

Si la rúbrica del docente cambia y exige que la IA sea una característica central, la prueba de concepto de la primera semana será una **puerta de decisión**: si no hay una alternativa viable sin coste, se renegocia el alcance o el requisito con el profesor. Con la rúbrica vigente, la IA es un diferenciador y no bloquea la entrega.

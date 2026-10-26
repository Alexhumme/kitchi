# 11 · Guion de la demostración académica — Kitchi Studio

Preparación de la exposición · Versión 1.0

> La exposición debe demostrar tanto el producto como las decisiones técnicas. Presentación recomendada de **8 a 12 minutos**, si el tiempo asignado por el profesor lo permite. Incluye resultados obtenidos durante las pruebas, **no cifras inventadas** ni demostraciones preparadas únicamente para aparentar concurrencia.

## Preparación previa (tareas P26 y P28)

- [ ] Datos de demostración cargados (`scripts/seed_demo_data.py`): cuentas de prueba, un personaje publicado y paquetes ya generados como respaldo.
- [ ] Backend, frontend y MySQL levantados y verificados minutos antes de exponer.
- [ ] Terminal lista para ejecutar las pruebas de concurrencia y el benchmark.
- [ ] Respaldo de capturas y resultados por si falla una demo en vivo (pero siempre distinguibles de la ejecución real).
- [ ] Ensayo completo cronometrado por al menos una persona distinta del ponente habitual.

## Bloques

### Bloque 1 — Producto y diseño (≈2 min)

- Mostrar el editor y modificar los seis atributos en vivo.
- Explicar cómo las capas mantienen la consistencia de marca.
- Mensaje clave: 18 opciones conceptuales + motor de composición, no 729 imágenes.

### Bloque 2 — Generación (≈2 min)

- Crear un paquete desde el personaje editado.
- Mostrar los seis PNG transparentes y cómo se descargan.
- Explicar cómo el motor compone los recursos en orden de capas y valida el resultado.

### Bloque 3 — Inteligencia artificial (≈2 min)

- Mostrar la entrada (fotografía), la ejecución del modelo, el resultado y el manejo de errores.
- Explicar la alternativa elegida (ADR-003), por qué se seleccionó y cómo funciona la contingencia si el servicio falla.
- Dejar claro qué es inferencia real y qué es simulado.

### Bloque 4 — Comunidad (≈2 min)

- Publicar un personaje con una cuenta.
- Abrir otra sesión, encontrarlo en el hub y copiarlo.
- Verificar en vivo que editar la copia **no** altera el original.

### Bloque 5 — Programación avanzada (≈3 min)

- Ejecutar la prueba concurrente (`asyncio`) y explicar el solapamiento de tareas de E/S.
- Comparar procesamiento secuencial y paralelo con los números reales del benchmark (aceleración observada).
- Explicar los procesos observados (multiprocesamiento, número de trabajadores, aislamiento de fallos).
- Responder con las definiciones de [08_CONCURRENCY_AND_PARALLELISM.md](08_CONCURRENCY_AND_PARALLELISM.md): concurrencia ≠ paralelismo ≠ multiprocesamiento.

## Cierre

Relacionar los cinco resultados del proyecto (defectos, decisiones, evidencias) con los criterios AC-01 … AC-14 de [02_REQUIREMENTS.md](02_REQUIREMENTS.md) y con la definición de éxito de [01_MASTER_PLAN.md](01_MASTER_PLAN.md#definición-final-del-éxito): producto, diseño, arquitectura, rigor académico y reproducibilidad.

## Registro de ensayos

| Fecha | Versión probada | Duración | Problemas detectados | Correcciones |
| --- | --- | --- | --- | --- |
| — | — | — | — | — |

# 11 · Guion de la sustentación académica — Kitchi Studio

Preparación de la exposición · Versión 1.1 · 28 de octubre de 2026

> La sustentación es el **miércoles 25 de noviembre de 2026**, en horario de clase. El profesor asigna **10 minutos por grupo**: demo en vivo + preguntas individuales. El guion debe ejecutarse completo en ese tiempo, no en 8–12 minutos. Incluye resultados obtenidos durante las pruebas, **no cifras inventadas** ni demostraciones preparadas únicamente para aparentar concurrencia.

## Preparación previa (tareas P26, P28 y P37)

- [ ] Datos de demostración cargados (`scripts/seed_demo_data.py`): cuentas de prueba, un personaje publicado y paquetes ya generados como respaldo.
- [ ] Backend, frontend, MySQL y Swagger levantados y verificados minutos antes de exponer.
- [ ] README y `/api/docs/` abiertos en pestañas separadas.
- [ ] Terminal lista para ejecutar las pruebas de concurrencia y el benchmark.
- [ ] Respaldo de capturas y resultados por si falla una demo en vivo (pero siempre distinguibles de la ejecución real).
- [ ] Ensayo completo cronometrado por al menos una persona distinta del ponente habitual.
- [ ] Cada integrante puede explicar un módulo ajeno y navegar el repositorio sin ayuda.

## Reparto del tiempo (10 minutos)

| Minuto | Bloque | Responsable sugerido | Qué se muestra |
| --- | --- | --- | --- |
| 0:00–1:00 | Problema y propuesta | Integrante A | Usuario, problema y flujo completo en una frase |
| 1:00–3:00 | Editor y stickers | Integrante A/C | Seis categorías, capas, generación y descarga de seis PNG |
| 3:00–4:30 | Backend y datos | Integrante B | API, MySQL, permisos, `/api/docs/` y persistencia |
| 4:30–6:00 | IA | Integrante C | Fotografía, inferencia real, resultado y contingencia |
| 6:00–7:30 | Comunidad y cierre | Integrante A/B | Publicar, explorar, copiar y verificar que el original no cambia |
| 7:30–10:00 | Preguntas individuales | Todo el equipo | Cada integrante responde sobre su módulo y el flujo general |

> Si el docente permite menos tiempo de preguntas, cerrar la demo en 7 minutos y dejar el resto para preguntas. Nunca sacrificar la demo funcional por una explicación teórica.

## Bloques

### Bloque 1 — Producto y problema (≈1 min)

- Mostrar la pantalla de inicio y explicar para quién es Kitchi Studio.
- Mensaje clave: no es un CRUD; es un editor visual que produce stickers reales y una comunidad para reutilizarlos.
- Mencionar las tres funcionalidades completas que se van a demostrar.

### Bloque 2 — Editor y generación (≈2 min)

- Modificar las seis categorías en vivo.
- Explicar cómo las capas mantienen la consistencia de marca.
- Mensaje clave: 18 opciones conceptuales + motor de composición, no 729 imágenes.
- Generar el paquete y abrir los seis PNG transparentes.

### Bloque 3 — Backend, datos y Swagger (≈1.5 min)

- Abrir `/api/docs/` y mostrar un endpoint.
- Explicar modelos, migraciones, permisos y límite de tres gatos.
- Mostrar que un dato persiste tras reiniciar o recargar.
- Mencionar `.env` y que no hay secretos en el repositorio.

### Bloque 4 — IA (≈1.5 min)

- Mostrar la entrada (fotografía), la ejecución del modelo, el resultado y el manejo de errores.
- Explicar la alternativa elegida (ADR-003), por qué se seleccionó y cómo funciona la contingencia si el servicio falla.
- Dejar claro qué es inferencia real y qué es simulado.

### Bloque 5 — Comunidad (≈1.5 min)

- Publicar un personaje con una cuenta.
- Abrir otra sesión, encontrarlo en el hub y copiarlo.
- Verificar en vivo que editar la copia **no** altera el original.
- Mostrar que un invitado no puede publicar.

### Bloque 6 — Calidad y evidencias (≈30 s)

- Mencionar las pruebas ejecutadas y el benchmark real (sin exagerar).
- Explicar la diferencia entre concurrencia, paralelismo y multiprocesamiento con los resultados obtenidos.
- Señalar el README, la guía viva y la auditoría académica.

## Preguntas individuales

Cada integrante debe poder responder, sin ayuda:

1. ¿Cuál es la arquitectura del proyecto y por qué se eligió?
2. ¿Cómo se guarda y valida la configuración de un gato?
3. ¿Cómo se generan los seis stickers y cómo se conserva la transparencia?
4. ¿Dónde se aplica el límite de tres gatos y por qué en el backend?
5. ¿Cómo se autoriza la copia de una publicación?
6. ¿Qué hace exactamente la IA y qué ocurre si falla?
7. ¿Dónde están las credenciales y cómo se cargan?
8. ¿Qué diferencia hay entre concurrencia, paralelismo y multiprocesamiento?
9. ¿Cómo se instala el proyecto desde cero?
10. ¿Qué parte del código no escribiste tú y cómo la explicarías?

## Cierre

Relacionar el proyecto con los cinco criterios de la rúbrica y con los criterios AC-01…AC-22 de [02_REQUIREMENTS.md](02_REQUIREMENTS.md):

- **Utilidad y alcance:** un usuario real obtiene stickers personalizados.
- **Funcionalidad:** las tres funcionalidades se ejecutan sin errores.
- **Calidad técnica:** módulos separados, `.env`, pruebas y código explicable.
- **Sustentación individual:** cada integrante domina su parte y el flujo general.
- **Repositorio y documentación:** README, guía viva, Swagger y auditoría.

## Plan de respaldo

- Si falla la red o el proveedor de IA: mostrar la contingencia y el flujo manual; no fingir una inferencia.
- Si falla MySQL: usar los datos de demostración ya cargados o el respaldo de capturas, indicando que es un respaldo.
- Si falla Flet: mostrar Swagger y los endpoints, y explicar la arquitectura.
- Si el tiempo se acorta: priorizar editor + stickers + comunidad; dejar la IA y el benchmark para preguntas.

## Registro de ensayos

| Fecha | Versión probada | Duración | Problemas detectados | Correcciones |
| --- | --- | --- | --- | --- |
| — | — | — | — | — |

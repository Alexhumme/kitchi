# ADR-007 — Hub de publicaciones (P18) y estilo "juguete"

- **Estado:** aceptado
- **Fecha:** 2026-11-16
- **Sustituye a:** —
- **Sustituida por:** —

## Contexto

Kitchi Studio necesita un hub público para cumplir el objetivo de producto (crear y hacer
visible un gato chibi) y la rúbrica de tres funcionalidades mínimas. Hasta el 10 de noviembre
`/api/publications/` respondía 404. El hub también es el primer lugar de la app donde la
previsualización del gato llega al usuario como tarjeta de contenido, y la primera interacción
con la API donde alguien publica en nombre de su cuenta.

A la vez se renovó el estilo visual (sustituyó la primera versión con bordes de 1px por
ubicaciones a un estilo más físico) y se evaluó la reproducción de sonidos en el cliente web.

## Decisión

1. **Publications y perfiles públicos en el backend, sin secretos ni ruteo de permisos.**
   - `GET /api/publications/` público (petición sin token): listado paginado del feed
     (`q=` filtra por título, descripción y autor; `user=` por nombre de usuario;
     `page_size` opcional). Devuelve siempre públicos, más las privadas del autor si
     hay sesión.
   - `POST /api/publications/` autenticado: `{cat_id, title, description, visibility}`.
     Errores: gato que no es tuyo → 403; ya publicado → 409
     (`PUBLICATION_ALREADY_EXISTS`); no existe → 404.
   - `GET /api/publications/{id}/`: pública; las privadas solo autor o admin.
   - `GET /api/profiles/{username}/` público: tarjeta con `username`, `joined_at`,
     `publication_count` y el listado de gatos y publicaciones visibles para el
     solicitante.
   - Serializers embeben una vista del gato (preview) para que las tarjetas no requieran
     una segunda llamada.
2. **Publicar se hace desde Mis gatos** (botón de compartir en cada tarjeta o Chip de
   "Publicado" si ya está publicado); no hay botón global de "publicar". Los invitados
   ven la acción pero, al intentar publicar, la app abre el diálogo de inicio de sesión.
3. **Feed de dos columnas con buscador.** Cada tarjeta es cuadrada, muestra el preview
   del gato (placeholders de color, pendiente de assets), el título y el autor (avatar +
   nombre); tocar el autor abre su perfil público. Flet 1.1.2 no pinta `Wrap`, así que
   el grid se rota en dos columnas alternadas (tarjetas visibles).
4. **Estilo "juguete" global.** Bordes sólidos de 3px en tinta, esquinas grandes,
   sombra dura desplazada (`ft.BoxShadow(offset=(0,4), blur_radius=0)`) y rebote al
   tocar (`EASE_OUT_BACK` + `animate_scale`). Los botones principales, papeletas, cards,
   banners y el diálogo se actualizan; los inputs usan OutlineInputBorder chunky.
5. **Retroalimentación táctil sí; sonido no.** Flet 1.1.2 no tiene control de audio ni
   acceso a Web Audio (`ft.HapticFeedback` vibra en móvil; el navegador no vibra y la
   web no emite audio desde Python). Se difiere la decisión de incluir sonidos a la
   versión del framework que soporte `ft.Audio` en web, o a un plugin/librería aprobada
   explícitamente por el equipo (p. ej. integrar `howler` vía un control propio).

## Consecuencias

- **Positivas:** el hub cumple P18; feed público filtrable; perfil público de autores;
  crear→publicar→feed verificado en navegador por CDP contra el servidor real;
  estilo coherente y más físico sin dependencias nuevas; testing del cliente y del
  backend cubre el contrato del feed (`qs=`, `user=`, perfiles).
- **Negativas:** esfuerzo duplicado entre render de previsualización del gato en editor
  y feed (ya comparten `cat_view` pero falta unificar); audio inexistente hasta Flet 1.2
  o decisión explícita; el embebido del gato en cada publicación duplica el payload.
- **Riesgos:** la autenticación del feed se mantiene pública (catálogo público de
  identidades — decidir si los perfiles públicos entran en P19 o P40). Re-evaluación
  de filtro y paginación al llegar assets reales de la diseñadora.

## Alternativas descartadas

- **Feed por usuario autenticado únicamente:** invita a publicar pero castiga la
  difusión y el descubrimiento; se descarta.
- **Publicaciones con un campo `preview_url` del gato:** obliga a renderizar en
  servidor; los renders son placeholders hasta P06, así que el embebido de configuración
  es más simple y honesto.
- **Incluir sonidos sintetizados con assets WAV:** requiere un control de audio que
  Flet 1.1.2 no expone en web; se descarta hasta que el framework lo soporte.

## Verificación

- `pytest` en `frontend/`: 46 pruebas en verde.
- `pytest` en `backend/`: 58 pruebas en verde.
- Verificación en vivo contra MySQL real (CDP, perfil de Chrome limpio): inicio de
  sesión UI, creación del gato, publicación, recarga y persistencia ("1 publicación
  pública"), buscador que filtra en vivo ("1 publicación pública" con luna), perfil
  público abre desde la tarjeta (muestra gtas + publicaciones).
- Informe y capturas: [`../reports/p18-hub-publicaciones.md`](../reports/p18-hub-publicaciones.md).

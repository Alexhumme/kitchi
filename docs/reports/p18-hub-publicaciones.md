# Informe — P18 · Hub de publicaciones (2026-11-16)

**Autor:** Alex Valdelamar · **Área:** frontend y backend (community) · **Versión:** v0.3.0 · **Evidencia:** ADR-007 + `.diag2/` del día (reproducible)

## Objetivo

1. Cerrar el recorrido público del producto: **crear gato → publicar → feed público**.
2. Abandonar el diseño con bordes delgados y pasar a un estilo físico/juguetón.
3. Verificar en navegador real que todo el flujo funciona con el backend real.

## Qué se hizo

**Backend**
- `apps/community/serializers.py`: `PublicationCatSerializer`, `PublicationReadSerializer`
  (autor embebido + gato) y `PublicationWriteSerializer` (`cat_id`, `title`, `description`,
  `visibility`).
- `apps/community/views.py`: `PublicationListCreateView` (GET: feed público paginado con
  `q=` por título/descripción/autor y `user=` por autor; POST autenticado, 409 si el gato
  ya está publicado, 403 si el gato no es tuyo), `PublicationDetailView` y
  `PublicProfileView` (`/api/profiles/<username>/`).
- `apps/community/urls.py` y `config/urls.py`: rutas `/api/publications/` (+ `{id}/`) y
  `/api/profiles/<username>/`.
- Pruebas en `backend/tests/test_community_api.py`: publicación, 403/409/404, privacidad,
  búsqueda, perfil público; **58 pruebas en verde**.
- `scripts/seed_catalog.py` se había vaciado de datos (0 opciones en MySQL); se resembró
  para poder ejercitar el flujo con datos reales.

**Frontend**
- `kitchi/feed_ui.py` (nuevo): tarjeta cuadrada compartida (avatar con inicial coloreada,
  preview con placeholder de color, título y nombre de autor clicable).
- `kitchi/screens/hub.py`: feed público: buscador con debounce, contador de publicaciones,
  estado vacío honesto, tarjetas de 2 columnas; el engranaje de la cabecera abre
  **Configuración** (acerca de, efectos, estado de la API, vaciado de datos locales).
- `kitchi/screens/public_profile.py`: perfil público navegable (miembro desde, gatos
  publicados, últimas publicaciones), accesible desde las tarjetas del feed.
- `kitchi/cat_view.py`: render provisional de gato para tarjetas (mismos colores del
  catálogo; se reemplazará por el render Pillow en P13).
- **Mis gatos**: botón de compartir en cada gato (solo cuentas; los invitados ven un
  diálogo de login/registro), diálogo para título/descripción/visibilidad (Switch) y chip
  "Publicado" cuando ya está publicado. `app.published_cat_ids` se carga en la sesión.
- **Estilo "juguete"**: bordes sólidos tinta (3 px), esquinas grandes, `BoxShadow(offset=(0,4), blur_radius=0)`,
  rebotes `EASE_OUT_BACK` al pulsar botones, hitos chunky y avatar de inicial por usuario.
- `kitchi/components.py`: `wire_tap` (háptica + rebote), `avatar()` y `field_shell()`
  reutilizable; botones e iconos con bordes y silueta del jugucte.
- **`SharedPreferences` "semantica muerta":** se encontró que la instancia `TextField`
  se re-creaba en cada `rebuild_current()`, destruyendo el nodo de Flet y dejando el
  input oculto sin foco (y `input.value` vacío para siempre tras un segundo carácter). Se
  conserva la instancia del campo entre rebuilds.
- `kitchi/storage.py` mapea preferencias de UI (`kitchi.ui.sound`, `kitchi.ui.animations`,
  `kitchi.ui.haptic`).
- Pruebas del frontend: **46 pruebas en verde** (cliente de publicaciones, perfiles,
  feed y chips/configuración de preferencias).

## Evidencia

| Archivo | Qué muestra |
| --- | --- |
| `p18-hub/feed-antes-de-publicar.png` | Navegar vacío con contador de 0 publicaciones |
| `p18-hub/feed-2-publicaciones.png` | Layout inicial del feed con dos publicaciones de cuentas de prueba |
| `p18-hub/feed-final-4-publicaciones.png` | Feed después de publicar desde la UI: 4 publicaciones |
| `p18-hub/dialogo-publicar.png` | Diálogo "Publicar en el hub" (título, descripción, visibilidad) |
| `p18-hub/configuracion.png` | Vista Configuración (acerca de, efectos, API, datos locales) |
| `p18-hub/perfil-publico.png` | Perfil público (tarjeta de usuario en el feed) |
| `p18-hub/mis-gatos-despues-de-publicar.png` | Mis gatos con chip "Publicado" |
| `p18-hub/limpiar-filtro.png` | Buscar "luna" filtra a 1 publicación pública |

## Límites y notas honestas

- **Sonido:** Flet 1.1.2 no puede reproducir audio en web; se descarta por ahora (ver ADR-007).
- **Autor, no hola:** la búsqueda hace `q=` con `icontains`; solo puede filtrar por substrings
  del título, la descripción y el nombre de usuario. Sin índice de texto completo (MySQL
  por defecto), suficiente para el volumen del prototipo.
- **Preview:** la tarjeta del feed dibuja el gato con contenedores de color (preview en
  tiempo real) porque no hay assets finales; no es Pillow ni una imagen real (mentira visual
  mínima y declarada en la guía).
- **Todos los datos de prueba eran cuentas `test-kitchi` temporales y se
  borraron los datos** (`flowpub1794870802`, `feeddemo1794869990`, `pubdemo1794872344`
  eliminadas vía `manage.py shell`); la base MySQL del desarrollador volvió a 0
  publicaciones / 0 gatos.
- **Verificación visual** se hizo con CDP headless (Chrome) + `flet_web.fastapi` para
  explorar sin dependencia de playwright; las interacciones principales (login, crea
  gato, publicar, feed) se ejercieron contra el servidor en ejecución.

# kitchi.studio — frontend-react (prototipo)

Interfaz web de Kitchi Studio reconstruida con **React 19 + TypeScript + Vite** y un sistema de
**diseño propio en CSS atomizado** (sin Tailwind), con la misma API Django REST Framework que
la versión Flet (`frontend/`). Nace como **prototipo de viabilidad** tras los límites encontrados
en Flet 1.1.2 (ver [`docs/decisions/ADR-006-flet-1-1-2-web-issues.md`](../docs/decisions/ADR-006-flet-1-1-2-web-issues.md)
y [`docs/decisions/ADR-009-react-frontend.md`](../docs/decisions/ADR-009-react-frontend.md)).

> La versión Flet (`frontend/`) sigue siendo la referencia de paridad y no se ha eliminado.
> Esta carpeta no está integrada aún en la entrega final: el equipo decidirá cuál interfaz se
> presenta en la sustentación.

## Requisitos

- Node.js 20+ y npm 10+ (verificado con Node 24.20.0 y npm 11.19.0).
- El backend Django en marcha en `http://127.0.0.1:8000` (ver el README raíz, sección 6).

## Ejecutar en desarrollo

```bash
cd frontend-react
npm install
npm run dev        # http://127.0.0.1:5173
```

El backend debe permitir el origen de Vite (`http://127.0.0.1:5173`). Desde P19 el valor por
defecto de `CORS_ALLOWED_ORIGINS` ya incluye 5173/4173; si tu entorno define la variable de
entorno `CORS_ALLOWED_ORIGINS` (p. ej. para la app Flet en 8550), añade también los orígenes
de Vite — un valor de variable de entorno tiene prioridad sobre el valor por defecto.

Para apuntar a otro backend, define `VITE_API_URL` antes de arrancar (p. ej. en un `.env.local`):

```bash
VITE_API_URL=http://127.0.0.1:8000 npm run dev
```

## Compilar y previsualizar

```bash
npm run build      # tsc -b + vite build → dist/
npm run preview    # http://127.0.0.1:4173
npm run lint       # oxlint
```

## Qué incluye (paridad funcional con el Flet)

| Área | Estado |
| --- | --- |
| Navegar (feed público, buscador con debounce, cargar más) | Implementado |
| Crear/Editar (6 categorías × 3 opciones, deshacer, reiniciar, aleatorio) | Implementado |
| Mis gatos (lista, editar, publicar con visibilidad, eliminar con deshacer en invitado) | Implementado |
| Stickers IA (poses reales de `/api/poses/`; generación pendiente P13–P16) | Implementado (honesto) |
| Perfil (cuenta e invitado) y Configuración (efectos, datos, acerca de) | Implementado |
| Registro/inicio de sesión contra `/api/auth/` y migración de gatos de invitado | Implementado |
| Perfil público `/publico/:username` | Implementado |
| Modo invitado con hasta 3 gatos en `localStorage` | Implementado |

Diferencias con la versión Flet:

- El gato se dibuja como **SVG** (conjunto completo: pelaje, cara, peinado, ropa y accesorio),
  no con placeholders de color por contenedores.
- Los iconos son **lucide-react** (trazo consistente y redondeado), no emojis.
- Hay **sonido real** sintetizado con Web Audio (`src/lib/fx.ts`) y vibración con
  `navigator.vibrate`; Flet 1.1.2 no podía reproducir audio en web.
- Las animaciones usan **framer-motion** (resortes en botones, transiciones de pantalla,
  píldora animada del tab activo).

## Verificación

- Flujo E2E por la UI real contra el backend: registro → crear gato → guardar → publicar →
  aparece en el feed (verificado el 2026-11-16).
- Capturas en `docs/reports/frontend-react.md`.
- `npm run build` y `npm run lint` limpios (sin errores; el lint deja dos avisos menores de
  `set-state-in-effect` aceptados para el fetch-on-param).

## Estructura

```
src/
  lib/catalog.ts       # catálogo empaquetado (fallback offline + validación)
  lib/api.ts           # cliente HTTP tipado a la API DRF
  lib/fx.ts            # sonido Web Audio + vibración
  state/AppContext.tsx # sesión, gatos (cuenta o invitado), feed, preferencias
  components/          # CatSVG, FeedCard, Avatar, ui (toasts, diálogo, toggles)
  screens/             # Hub, Editor, Mis gatos, Stickers IA, Perfil, Configuración, Auth, Perfil público
  styles/              # CSS atomizado (globals, layout, components/, screens/)
```

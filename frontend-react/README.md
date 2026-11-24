# kitchi.studio — frontend React

Interfaz web de Kitchi Studio construida con **React 19 + TypeScript + Vite** y un sistema de
**diseño propio en CSS atomizado** (sin Tailwind). Consume la API Django REST Framework y es la
única interfaz activa del proyecto desde el 23 de noviembre de 2026
([`ADR-011`](../docs/decisions/ADR-011-react-interfaz-definitiva.md)). La implementación Flet se
retiró; sus reportes y ADR se conservan como historial.

## Requisitos

- Node.js 20+ y npm 10+ (verificado con Node 24.22.1 y npm 11.19.0).
- El backend Django en marcha en `http://127.0.0.1:8000` (ver el README raíz, sección 6).

## Ejecutar en desarrollo

```bash
cd frontend-react
npm install
npm run dev        # http://127.0.0.1:5173
```

El backend debe permitir el origen de Vite (`http://127.0.0.1:5173`). El valor por
defecto de `CORS_ALLOWED_ORIGINS` incluye 5173/4173; si defines esa variable de entorno,
añade también los orígenes de Vite — un valor de variable de entorno tiene prioridad sobre el valor por defecto.

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

## Qué incluye

| Área | Estado |
| --- | --- |
| Navegar (feed público, buscador con debounce, cargar más) | Implementado |
| Crear/Editar (pelaje, ojos, 10 peinados, 6 superiores, 6 inferiores y 13 accesorios; deshacer, reiniciar, aleatorio) | Implementado |
| Mis gatos (lista, editar, publicar con visibilidad, eliminar con deshacer en invitado) | Implementado |
| Stickers IA (poses reales de `/api/poses/`; generación pendiente P13–P16) | Implementado (honesto) |
| Perfil (cuenta e invitado) y Configuración (efectos, datos, acerca de) | Implementado |
| Registro/inicio de sesión contra `/api/auth/` y migración de gatos de invitado | Implementado |
| Perfil público `/publico/:username` | Implementado |
| Modo invitado con hasta 3 gatos en `localStorage` | Implementado |

## Editor visual

- El gato usa los **SVG reales** del cuerpo, cabello delantero/trasero, prendas y accesorios.
  La cabeza se renderiza después de la prenda superior y antes del cabello delantero, de modo
  que cuellos y solapas quedan detrás de la cara.
- La cabeza delantera y el cuello de las prendas se verificaron en el lienzo y en los seis
  previews el 23 de noviembre; el `viewBox` ampliado mantiene pies, cabello y accesorios dentro
  del encuadre. Evidencia en [`docs/reports/editor-visual-assets.md`](../docs/reports/editor-visual-assets.md).
- Incluye sliders de color, un mini slider independiente en cada accesorio seleccionado,
  previews reales y multiaccesorio con exclusión por tipo. Los colores de accesorios se guardan
  por separado. Las texturas de pelaje siguen sin implementarse.
- Los iconos son **lucide-react** (trazo consistente y redondeado).
- Hay **sonido real** sintetizado con Web Audio (`src/lib/fx.ts`) y vibración con
  `navigator.vibrate`.
- Las animaciones usan **framer-motion** (resortes en botones, transiciones de pantalla,
  píldora animada del tab activo).

## Verificación

- Flujo E2E por la UI real contra el backend: registro → crear gato → guardar → publicar →
  aparece en el feed (verificado el 2026-11-16).
- Evidencia del editor y capturas de la cabeza/cuello en
  [`docs/reports/editor-visual-assets.md`](../docs/reports/editor-visual-assets.md); historial de
  la interfaz en [`docs/reports/frontend-react.md`](../docs/reports/frontend-react.md).
- `npm run build` pasa y `npm run lint` no tiene errores (mantiene dos avisos menores de
  `set-state-in-effect`).

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

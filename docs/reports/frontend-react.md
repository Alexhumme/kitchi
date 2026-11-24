# Interfaz React (`frontend-react/`) — evidencia histórica y estado actual

> **Estado actual (23 de noviembre de 2026):** React es la única interfaz activa
> ([ADR-011](../decisions/ADR-011-react-interfaz-definitiva.md)). Flet y sus pruebas se
> retiraron del árbol de entrega. Las secciones siguientes conservan la evidencia del
> incremento original y sus resultados históricos; no describen una segunda interfaz vigente.

Prototipo de viabilidad construido tras el pivot del 16 de noviembre de 2026 (ADR-009):
el Flet 1.1.2 no era capaz de concretar los estilos deseados (ADR-006). Este documento
registra qué se hizo, cómo se verificó y qué falta.

## Alcance

- Carpeta nueva `frontend-react/` en la rama `feat/frontend-react`; `frontend/` (Flet) intacta.
- Mismo backend Django REST Framework y MySQL; **sin cambios de esquema ni contratos**.
- Paridad funcional completa: Navegar (feed público, buscador con debounce, cargar más),
  Crear/Editar (6×3, deshacer, reiniciar, aleatorio), Mis gatos (publicar con visibilidad,
  deshacer eliminación en invitado), Stickers IA (poses reales, honestidad P13–P16), Perfil,
  Configuración (efectos reales: sonido Web Audio + vibración), registro/login contra
  `/api/auth/`, migración de gatos de invitado, perfil público `/publico/:username`.
- ~~Tailwind~~ Sistema de diseño propio en CSS atomizado (`src/styles/`: globals.css, layout.css,
  components/{bevels,toolbar,forms,cards,ui}.css, screens/{hub,editor,my-cats,stickers,profile,settings,auth,public-profile}.css,
  y `src/styles/index.css` como hoja de imports. Tailwind v4 se eliminó el 2026-11-17 porque la
  mezcla de utilidades y clases propias hacía muy difícil la edición manual de los estilos.
- `framer-motion` (resortes, transiciones, píldora activa); `lucide-react`; gato SVG completo.
- `CORS_ALLOWED_ORIGINS` une por defecto 5173/4173 (`settings.py`) con los orígenes definidos
  en el entorno; una variable de entorno no elimina los orígenes locales de React.

## Verificación

| Comprobación | Resultado | Fecha |
| --- | --- | --- |
| `npm run build` (tsc + vite build) | Limpio (467 módulos, 148 kB gzip) | 2026-11-16 |
| Fuente Fredoka cargando de verdad | La primera versión usaba `tech("variations")` dentro de `src`: Chromium descartaba la declaración (`document.fonts.size: 0`). Corregido a `format("truetype-variations")` con rango `300 700` (el real del archivo); `document.fonts.size: 1` y el TTF se descarga | 2026-11-16 |
| `npm run lint` (oxlint) | Sin errores; 2 avisos `set-state-in-effect` aceptados | 2026-11-16 |
| Registro → Crear → Guardar → Publicar → feed (E2E por CDP contra el backend real) | `["Diagatito","Lolopepe"]` en `/api/publications/`; datos de prueba borrados tras verificar (gato borrado ⇒ publicación borrada en cascada) | 2026-11-16 |
| Pruebas Flet | 46 en verde (sin tocar `frontend/`) | 2026-11-16 |
| Pruebas backend | 58 en verde (sin tocar lógica de negocio) | 2026-11-16 |
| Viewport 430×900 (emulación CDP) | Layout sin desbordes; barras y marco correctos | 2026-11-16 |
| Mis gatos coleccionable (grid/list, filtros Todos/Publicados/Borradores, menú ⋯, hueco "Crear otro gato") | Verificado con 2 gatos de invitado por la UI real; "Borradores (2)" filtra bien; el flujo de crear → guardar → ver en Mis gatos sigue funcionando | 2026-11-17 |
| Admin sin límite de gatos (RBAC) | Backend: test de 5 gatos con `admin_client` (`tests/test_cats.py::test_admin_no_tiene_limite_de_gatos`), suite 59 en verde; frontend: creación por UI superando 3/3 con cuenta admin de prueba (`admintest_e2e`, borrada luego) y captura del perfil ("Plan Admin · sin límites"); datos de prueba eliminados | 2026-11-17 |
| Perfil público rediseñado (credencial pública, gatos publicados, publicaciones) | Verificado con la cuenta real alexvb: métricas Gatos/Publicados/Días aquí correctas, gatos SVG renderizan, chip de hora relativa, sin datos privados; capturas en `docs/reports/frontend-react/perfil-publico.png` | 2026-11-17 |
| Settings rediseñado (cabecera flat, secciones duras, tech chips, toggles con iconos de color) | Verificado visualmente (captura `configuracion.png` actualizada); 2 avisos de lint conocidos sin cambios | 2026-11-17 |
| Acceso rediseñado (sol miel, chip KITCHI.STUDIO, anillo miel en foco, CTA con flecha, invitado como botón blanco) | Verificado en login y registro (ambos modos); captura `acceso.png` | 2026-11-17 |
| Perfil rediseñado (credencial, Plan gratuito con barra de capacidad, accesos tiles) | Verificado con sesión real (cuenta de prueba perfiledemo_e2e, luego borrada) y con invitado; métricas reales (Gatos/Publicados/Días aquí); "Límite alcanzado" solo aparece al 3/3; CTA de ilimitados deshabilitada como Pronto; Cerrar sesión intacto | 2026-11-17 |
| Explorar rediseñado (post cards con hora relativa, stage tintado, chips, CTA al perfil público) | Verificado con las 2 publicaciones reales del hub (elena y KOKO, con hora relativa "Hace 38 min"); perfil público también usa el nuevo diseño; captura en `docs/reports/frontend-react/feed.png` | 2026-11-17 |

Capturas (430×900): [`navegador.png`](frontend-react/navegador.png) ·
[`crear.png`](frontend-react/crear.png) · [`publicar-modal.png`](frontend-react/publicar-modal.png) ·
[`configuracion.png`](frontend-react/configuracion.png)

## Diferencias frente a Flet (a favor)

- Gato completo en SVG: pelaje, ojos, peinados, ropa superior/inferior y accesorio.
- Sonido real (Web Audio) y vibración real (`navigator.vibrate`).
- Iconos lucide (trazo uniforme) en lugar de emojis; tab bar con píldora animada.
- Bundle estático; sin ciclo cliente-servidor de Flet Web.

## Pendiente honesto al cierre del incremento original

> Las afirmaciones de esta sección corresponden al 16–17 de noviembre. La adopción de
> React y la retirada de Flet quedaron resueltas el 23 de noviembre por ADR-011.

- La entrega académica sigue declarando Flet (cumplimiento, AR-01); migrar en firme exige
  decidirlo en equipo y actualizar README, cumplimiento y guía viva.
- Stickers IA: igual que en Flet, el motor (P13–P16) no existe; la pantalla lo declara.
- Equipo: el prototipo lo construyó solo una persona; la integración con los otros tres
  integrantes está por planificar (reparto de módulos).
- Dos avisos de lint no críticos; chunk grande (framer-motion + lucide) aceptable para el scope.

## Incremento de editor visual — 2026-11-23

El editor pasó a usar los SVG reales de cuerpo, cabello dividido, prendas y accesorios.
Incorpora sliders de color, un mini slider propio en el borde inferior de cada accesorio
seleccionado, previews reales por opción y combinaciones multiaccesorio con exclusividad por
tipo. El backend amplía de forma aditiva el esquema 1 con `accessories[].color`, conserva los
colores independientes y mantiene el espejo `accessory: {code}` para datos y clientes legacy.

La verificación completa, los resultados de navegador, MySQL y las limitaciones están en
[`editor-visual-assets.md`](editor-visual-assets.md). Al cierre del 23 de noviembre, el build
sigue limpio, lint mantiene los dos avisos conocidos y la suite vigente tiene 66 pruebas
backend; las 46 pruebas Flet son históricas y ya no se ejecutan. React es la única interfaz
activa y la cabeza delantera se renderiza sobre la prenda superior.

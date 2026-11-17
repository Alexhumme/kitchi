# Interfaz React (`frontend-react/`) — evidencia del incremento 2026-11-16

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
- `CORS_ALLOWED_ORIGINS` incluye por defecto 5173/4173 (settings.py); una variable de entorno
  con ese nombre tiene prioridad (ver ADR-009).

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

Capturas (430×900): [`navegador.png`](frontend-react/navegador.png) ·
[`crear.png`](frontend-react/crear.png) · [`publicar-modal.png`](frontend-react/publicar-modal.png) ·
[`configuracion.png`](frontend-react/configuracion.png)

## Diferencias frente a Flet (a favor)

- Gato completo en SVG: pelaje, ojos, peinados, ropa superior/inferior y accesorio.
- Sonido real (Web Audio) y vibración real (`navigator.vibrate`).
- Iconos lucide (trazo uniforme) en lugar de emojis; tab bar con píldora animada.
- Bundle estático; sin ciclo cliente-servidor de Flet Web.

## Pendiente honesto

- La entrega académica sigue declarando Flet (cumplimiento, AR-01); migrar en firme exige
  decidirlo en equipo y actualizar README, cumplimiento y guía viva.
- Stickers IA: igual que en Flet, el motor (P13–P16) no existe; la pantalla lo declara.
- Equipo: el prototipo lo construyó solo una persona; la integración con los otros tres
  integrantes está por planificar (reparto de módulos).
- Dos avisos de lint no críticos; chunk grande (framer-motion + lucide) aceptable para el scope.

# ADR-009 — Frontend React en paralelo a Flet (verificación de viabilidad)

- **Estado:** sustituido por [ADR-011](ADR-011-react-interfaz-definitiva.md)
- **Fecha:** 2026-11-16
- **Sustituye a:** —
- **Sustituida por:** ADR-011

## Contexto

Tras la integración del hub P18 y el rediseño Wonder en la versión Flet, la dirección del
proyecto pidió explícitamente abandonar esa vía: los estilos deseados eran "imposibles de
concretar con Flet". Los límites reales constatados están en
[`ADR-006-flet-1-1-2-web-issues.md`](ADR-006-flet-1-1-2-web-issues.md): render frágil en web,
controles que fallan silenciosamente, sin audio en la versión 1.1.2, y muy poco control fino
sobre esquinas, patrones, scroll y animaciones.

Reescribir la interfaz a mitad de ciclo tiene riesgo real con una fecha límite dura
(miércoles 25 de noviembre, 12:00 m.). Por eso la decisión se acota: se construye una **paridad
funcional completa** en React como **prototipo de viabilidad**, sin eliminar ni dejar de
mantener el Flet hasta que el equipo decida la interfaz final.

## Decisión

1. **Carpeta nueva `frontend-react/`**; `frontend/` (Flet) queda intacta como referencia y
   requisito académico (README declara Flet) hasta decisión explícita del equipo.
2. **Stack:** Vite 8 + React 19 + TypeScript estricto, con un **sistema de diseño propio en
   CSS atomizado** (`src/styles/`: globals, layout, components/, screens/). El prototipo arrancó
   con Tailwind v4 como utilidades sobre clases bevel propias; el 2026-11-17 se eliminó porque
   la mezcla de utilidades y clases propias hacía muy difícil la edición manual. `framer-motion`
   para animaciones de resorte y transiciones, `lucide-react` para iconos de trazo redondo y
   consistente, `react-router-dom` para rutas.
3. **Mismo backend y mismos contratos:** la app React consume la misma API DRF (`/api/auth/*`,
   `/api/catalog/`, `/api/poses/`, `/api/cats/`, `/api/publications/`, `/api/profiles/{username}/`)
   y respeta el mismo catálogo (`schema_version=1`). Ningún cambio de esquema ni de contratos.
4. **Cambios de comportamiento deliberados** frente al Flet:
   - El gato se dibuja como **SVG** completo (incluye ropa, peinados y accesorios que el Flet solo
     insinuaba).
   - El sonido es real (Web Audio) y la vibración usa `navigator.vibrate`; el Flet no podía.
   - El modo invitado mantiene el límite de 3 gatos en `localStorage` y migra al entrar, igual
     que el Flet.
5. **CORS:** `CORS_ALLOWED_ORIGINS` incluye por defecto 5173 (dev) y 4173 (preview). Una variable
   de entorno definida en la máquina **tiene prioridad** sobre el valor por defecto; en ese caso
   hay que añadir los orígenes de Vite a la variable.

## Consecuencias

- **Positivas:** HTML/CSS/JS abre animaciones con resortes, scroll suave, patrones y control de
  layout imposible en Flet 1.1.2; el gato SVG es resolución-independiente; bundle final ≈ 148 kB
  gzip (más fuente); el equipo decide la interfaz final con evidencia, no con suposiciones.
- **Negativas/pendientes:**
  - Dos frontends en el repositorio hasta la decisión final (coste de mantenimiento acotado a 9 días).
  - La entrega académica declara Flet como interfaz (cumplimiento 13_CUMPLIMIENTO_ACADEMICO.md,
    fila AR-01); cambiar la interfaz definitiva requiere actualizar README, guía viva y este ADR
    antes de la sustentación.
  - `npm run lint` deja dos avisos `set-state-in-effect` aceptados (fetch on route param); no son errores.

## Verificación

- `npm run build` (tsc + vite build) limpio; `npm run lint` sin errores.
- E2E por la UI real contra el backend local: registro → Crear → Guardar → Mis gatos → Publicar →
  aparece en el feed; datos de prueba eliminados tras la verificación (2026-11-16).
- Capturas en `docs/reports/frontend-react.md`.
- 46 pruebas Flet y 58 de backend siguen en verde.

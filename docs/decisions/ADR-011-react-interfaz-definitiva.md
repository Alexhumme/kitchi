# ADR-011 — React como interfaz definitiva y retirada de Flet

- **Estado:** aceptado
- **Fecha:** 2026-11-23
- **Sustituye a:** ADR-009
- **Sustituida por:** —

## Contexto

React alcanzó paridad funcional con Flet y superó sus limitaciones de diseño, audio y control de animaciones. El editor visual usa los SVG reales de la diseñadora y permite personalizar colores y combinar accesorios, capacidades que Flet no ofrecía. Mantener dos interfaces activas dejaría documentación y rutas de instalación divergentes.

## Decisión

1. `frontend-react/` es la única interfaz web del producto. Su stack es Vite 8, React 19, TypeScript estricto, CSS propio, `framer-motion`, `lucide-react` y `react-router-dom`.
2. Se retira `frontend/` (Flet), incluidas sus pruebas y recursos duplicados. Las pruebas Flet históricas se conservan únicamente como evidencia de incrementos anteriores.
3. React consume el mismo backend Django REST Framework, el mismo catálogo y el mismo esquema de configuración. La validación y la autorización siguen en el backend.
4. El espejo `accessory: {code}` se conserva por compatibilidad de datos y contratos, no porque exista una interfaz Flet activa.
5. La instalación, el README, la guía viva, el checklist y el cumplimiento académico declaran React como interfaz real.

## Consecuencias

- Hay una sola interfaz que instalar, probar y explicar durante la sustentación.
- La verificación automatizada vigente son 66 pruebas backend, build de React y lint de React; las 46 pruebas Flet son históricas y ya no se ejecutan.
- CORS mantiene los orígenes 5173/4173 para desarrollo y preview. El origen 8550 puede retirarse cuando se confirme que ningún despliegue lo usa.
- El motor Pillow, los seis PNG, la copia de publicaciones y la IA siguen pendientes; cambiar de interfaz no los convierte en funcionalidades terminadas.

## Verificación

- Build de React y lint sin errores; dos avisos `set-state-in-effect` conocidos.
- Suite backend: 66 pruebas aprobadas.
- Navegador: editor, previews, guardado y persistencia verificados previamente; la cabeza delantera se verificó sobre prendas con cuello el 23 de noviembre.

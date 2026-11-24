# ADR-010 — Configuración visual compatible con prendas coloreadas y accesorios múltiples

- **Estado:** aceptado
- **Fecha:** 2026-11-23
- **Sustituye a:** —
- **Sustituida por:** —

## Contexto

La diseñadora entregó los SVG reales del cuerpo, el cabello dividido en capas delantera/trasera, prendas y accesorios. El editor React debe permitir cambiar el color de cabello, prendas y accesorios, mostrar previews reales y combinar varios accesorios salvo cuando comparten un tipo (por ejemplo, dos coronas). Cada accesorio seleccionado tendrá un mini slider de tono en el borde inferior de su tarjeta.

El contrato inicial solo guardaba un accesorio y no aceptaba colores en `top` ni `bottom`. La extensión debe conservar los documentos guardados y el campo legacy `accessory`; Flet fue la interfaz que originalmente motivó ese espejo, pero quedó retirado por [ADR-011](ADR-011-react-interfaz-definitiva.md).

## Decisión

1. Se conserva `schema_version: 1`. La extensión es aditiva y los documentos antiguos siguen siendo válidos.
2. Las categorías `fur`, `eyes`, `hair`, `top` y `bottom` se guardan como objetos `{code, ...colores}`. Se permiten `top.color` y `bottom.color`.
3. Los accesorios se guardan en `accessories: [{code, color?}]`. `color` es opcional, hexadecimal de 6 u 8 dígitos e independiente para cada accesorio; si falta, React usa el color base del catálogo. El backend devuelve además `accessory: {code}` con el primer accesorio como espejo compatible; los clientes nuevos leen `accessories`. Una lista vacía no admite el espejo legacy.
4. `catalog_options.compatibility_group` identifica accesorios mutuamente excluyentes. El backend rechaza dos accesorios del mismo grupo y códigos repetidos.
5. La semilla del catálogo registra los códigos y rutas de los assets reales. Las texturas de pelaje no se dibujan hasta que la diseñadora las entregue.
6. Los SVG se preparan sin convertir clases de Illustrator en dependencias del navegador. Solo se tintan los rellenos base identificados de cabello, prendas y accesorios; los blancos de detalle conservan su color y el lienzo permanece transparente. El mini slider no se anida dentro del botón de selección para evitar que arrastrarlo también cambie la selección.
7. La cabeza base se renderiza como capa delantera después de la prenda superior y antes del cabello delantero. Así el cuello y las solapas de `top` quedan detrás de la cabeza; el cuerpo completo sigue sirviendo como base posterior para conservar su alineación.

## Consecuencias

- Los gatos antiguos se normalizan al abrirlos: el `accessory` legacy se convierte en una lista de un elemento.
- Los documentos antiguos se normalizan al abrirlos: el `accessory` legacy se convierte en una lista de un elemento. El espejo se conserva por compatibilidad de datos, no por una interfaz Flet activa.
- La API y el editor comparten la validación de catálogo, colores y grupos, sin aceptar rutas de archivo enviadas por el cliente.
- Se añade una migración no destructiva a `catalog_options`; no se modifican migraciones aplicadas ni datos existentes.

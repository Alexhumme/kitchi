# ADR-008 — Estilo "Super juguete": bevel asimétrico y patrones propios

- **Estado:** aceptado
- **Fecha:** 2026-11-16
- **Sustituye a:** ADR-006 §tema juguetón (se amplía, no se deroga)
- **Sustituida por:** —

## Contexto

El estilo juguetón acordado en ADR-006 era funcional (bordes gruesos, tema claro) pero
carecía de personalidad y de profundidad: todos los paneles tenían la misma silueta, la
barra inferior sólo usaba `NavigationBar` con el fondo por defecto, y los patrones
culturales de identidad (halftone dots, damero, estrellas, ondas, burbujas) no existían.

## Decisión

Adoptar un lenguaje visual inspirado en **Super Mario Wonder**, documento en tres partes.

1. **Bevel asimétrico + bevel de estética Wonder.** Todos los contornos llevan ancho 0
   arriba y a la izquierda y un canto grueso abajo y a la derecha, más una sombra dura
   desplazada sin desenfoque (`ft.BoxShadow(offset=(0,4), blur_radius=0)`). Esto genera
   volumen sin necesidad de gradientes pesados ni librerías externas. Los tokens viven en
   `frontend/src/kitchi/theme.py` (`RADIO_*`, `bevel()`, `SOMBRA*`, `pattern_image()`).
2. **Patrones propios del repositorio.** Se generan PNGs semitransparentes con Pillow en
   `scripts/generate_ui_patterns.py` y se cachean en `frontend/assets/ui/patterns/` y
   `frontend/assets/ui/separators/`: dots, damero, cruces, estrellas, burbujas, ondas sin kinks,
   arcoíris, zig-zag. Los separadores usan `ImageByRepeat` con `ui/separators/*.png`.
3. **Barra de herramientas y barra inferior distintas al cuerpo.** La cabecera usa
   `PANEL` (dorado miel) con un separador zig-zag; la barra inferior usa `INK` con un
   indicador `PANEL` y bandas arcoíris como firma de sección.

## Consecuencias

- **Positivas:** la interfaz gana personalidad reconocible; los bevels marrón-dorado dan
  profundidad sin imágenes raster pesadas; los botones son `FilledButton`/`OutlinedButton`
  nativos y conservan accesibilidad (texto + semantics), lo que mantiene el recorrido por
  teclado y lector de pantalla.
- **Negativas/pendientes:** el `ft.Row` envolvente todavía no implementa wrap; los
  patrones no escalan mejor de 48px; el patrón de ondas sólo se extiende en X.

## Verificación

46 pruebas en verde. Capturas CDP del recorrido (Navegar, Mis gatos, Crear, Stickers IA,
Perfil, Configuración) mostrando el nuevo sistema de bevel, patrones y barras oscuras; ver
`docs/reports/p18-hub-publicaciones.md`.

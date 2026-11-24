# 06 · Sistema visual y motor gráfico 2D — Kitchi Studio

Recursos gráficos, orden de capas y contrato entre diseño y desarrollo · Versión 1.3 · 23 de noviembre de 2026

> Esta es la parte central del producto. La aplicación **no** almacena una ilustración diferente para cada combinación: almacena una configuración del personaje y reconstruye su apariencia usando recursos gráficos ([ADR-002](decisions/ADR-002-character-rendering.md)).

## Estructura conceptual del personaje

Un personaje se define mediante un documento de configuración (esquema y validación en [04_DATA_MODEL.md](04_DATA_MODEL.md)). Las claves definitivas deben coincidir con los recursos que produzca la diseñadora.

## Organización de los recursos gráficos

```
assets/
├── characters/
│   ├── base/
│   ├── fur/
│   ├── eyes/
│   ├── hair/
│   ├── tops/
│   ├── bottoms/
│   └── accessories/
├── poses/
│   ├── greeting/
│   ├── happy/
│   ├── angry/
│   ├── sad/
│   ├── surprised/
│   └── sleepy/
├── ui/
└── catalog.json
```

La estructura exacta de carpetas puede cambiar según el formato de las ilustraciones. Lo importante es que **cada recurso tenga un identificador estable** y metadatos que indiquen:

- Categoría y variante.
- Orden de composición.
- Anclaje y posición.
- Compatibilidad con otras piezas.
- Paleta o tintado permitido.
- Licencia y autoría del recurso.

`assets/catalog.json` será el inventario de autoría y aprobación. Mientras se completa, el
backend valida contra `catalog_options` ([04_DATA_MODEL.md](04_DATA_MODEL.md)) y la semilla
`scripts/seed_catalog.py` registra 53 códigos con rutas relativas de los SVG reales. El editor
React los declara en `frontend-react/src/lib/characters.ts`.

## Orden de composición

El orden es explícito. El render actual del editor React usa:

1. Cabello trasero.
2. Cuerpo, cara, ojos y cola.
3. Parte inferior.
4. Parte superior.
5. Cabeza delantera, con pelaje y ojos.
6. Cabello delantero.
7. Accesorios seleccionados, en el orden de la lista.
8. Elementos gráficos del sticker cuando exista el motor de exportación.

La cabeza se superpone después de `top` para que cuellos y solapas no crucen la cara. El
cuerpo completo permanece como capa posterior para conservar la alineación de orejas, cola
y extremidades; no se divide ni se regenera su SVG.

El lienzo de referencia es el `viewBox` `0 -10 206.068 270`. Cada asset declara su anclaje
en `characters.ts`; el render lo convierte en `translate(...) scale(...)` para conservar la
posición relativa. Las prendas son capas completas, por lo que no se duplican partes del cuerpo.

## Contrato entre diseño y desarrollo

La diseñadora no entrega imágenes aisladas sin especificaciones. Desde la primera semana el equipo acuerda:

- [x] Un lienzo y una resolución base comunes.
- [x] El centro de referencia y las coordenadas de cada capa.
- [x] Un sistema coherente de nombres de archivos.
- [x] Una convención de transparencia.
- [x] Reglas de superposición.
- [ ] Una lista de recursos obligatorios para el primer paquete.
- [ ] Una hoja de control de recursos aprobados y pendientes.

**Criterio de la primera entrega gráfica:** debe incluir un personaje completo que pueda componerse técnicamente. Es preferible un gato completo con pocas opciones que seis categorías incompletas.

### Implementación visual vigente (23 de noviembre)

- El cabello se compone con dos SVG independientes: parte trasera y delantera. El color del
  peinado se aplica a ambas capas. Entre la prenda superior y el cabello delantero se renderiza
  `base/avatar_head.svg`, alineado con la cabeza del cuerpo y pintado con el pelaje y los ojos
  elegidos.
- El usuario cambia el tono de cabello, parte superior y parte inferior con un slider. Si el
  color actual es blanco, negro o gris, el primer movimiento introduce saturación y luminosidad
  visibles en lugar de dejar el tono sin efecto.
- Cada accesorio seleccionado tiene su propio mini slider de tono en el borde inferior de la
  tarjeta. El control es hermano del botón de selección, no está anidado en él; cambia el
  preview y el lienzo sin seleccionar ni quitar el accesorio. Los colores son independientes.
- Cada botón de opción renderiza el gato real con esa prenda o peinado; no usa una muestra de
  color plana. El preview y el lienzo principal comparten `CatSVG`.
- Se pueden combinar varios accesorios. El backend y el editor sustituyen automáticamente uno
  nuevo si ya existe otro del mismo `compatibility_group`; “Ninguno” vacía la selección.
- Los SVG se importan como texto y las clases de Illustrator se convierten en atributos
  `fill`/`stroke`. Solo se tintan los rellenos base de prenda, cabello o accesorio; los blancos
  de detalle se conservan y no se añade un rectángulo de fondo.
- No se dibujan texturas, rayas ni manchas de pelaje hasta que la diseñadora entregue esos
  recursos. La variación actual de pelaje se limita a los colores base y secundario.

## Generación de stickers

El motor recibe una configuración válida del personaje y un identificador de pose. Para cada pose:

1. Carga las capas necesarias.
2. Comprueba que los recursos existan.
3. Compone las imágenes en el orden definido.
4. Aplica colores cuando corresponda.
5. Ajusta el resultado al lienzo final.
6. Conserva el canal alfa.
7. Guarda el PNG.
8. Verifica dimensiones, transparencia y existencia del archivo.

La función principal debe ser **determinista**: la misma configuración y la misma versión de los recursos producen el mismo resultado, salvo aleatoriedad deliberada.

## Especificación de exportación

Para el prototipo:

| Propiedad | Valor |
| --- | --- |
| Formato | PNG RGBA |
| Fondo | Transparente |
| Dimensión inicial de trabajo | 512 × 512 píxeles |
| Perfil de color | sRGB cuando sea posible |
| Nombre de archivo | Identificador del paquete, pose y versión |
| Validación | Seis archivos válidos por paquete completado |

> Los 512 × 512 son una decisión de trabajo para la demostración, no una garantía para integraciones futuras. Los requisitos específicos de WhatsApp se revisan solo si más adelante se implementa la importación directa de paquetes (fuera del MVP).

## Criterios de diseño para la evaluación

La rúbrica valora que el producto sea utilizable por alguien que no programa y que la demo fluya sin errores. El diseño debe cubrir:

- **Móvil primero:** el editor y el hub deben funcionar en una pantalla pequeña sin controles inaccesibles.
- **Consistencia visual:** las opciones del primer paquete comparten proporciones, paleta y estilo; no se mezclan ilustraciones incompatibles.
- **Estados completos:** cada pantalla debe tener estado de carga, vacío, error y éxito. Un fallo visible y comprensible cuenta para el criterio 2.
- **Feedback inmediato:** al cambiar una categoría, el personaje se actualiza; al generar, se muestra progreso; al descargar, se confirma el resultado.
- **Accesibilidad básica:** contraste suficiente, textos legibles, controles con etiquetas y navegación clara.
- **Recursos originales o con licencia:** no se copian personajes, interfaces ni stickers de terceros sin permiso. La autoría y licencia se registran en `assets/catalog.json`.
- **Evidencias visuales:** capturas del editor, del paquete y del hub para el README y la sustentación.
- **Commits de la diseñadora:** los recursos, la guía visual y los ajustes de diseño se registran con commits propios y descriptivos.

## Estado

- Guía visual y proporciones: **implementadas en el editor React** con los SVG entregados;
  falta aprobar la hoja de control y la lista de recursos del primer paquete (P06).
- Previsualización: React compone el personaje real por capas, con previews por opción,
  colores y accesorios múltiples. La implementación Flet quedó retirada (ADR-011).
- Primer gato componible: **verificado en React** (23 de noviembre); el motor Pillow sigue
  pendiente (P04/P13).
- Formato de recursos del editor: SVG con anclajes y colores tintables. La exportación final
  de stickers seguirá siendo PNG RGBA cuando exista P13/P14.
- Capturas para README y sustentación: el editor y el orden cabeza/cuello ya tienen capturas
  ([`reports/editor-visual-assets.md`](reports/editor-visual-assets.md)); la demostración integral
  sigue pendiente (P31/P37).

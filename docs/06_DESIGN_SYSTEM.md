# 06 · Sistema visual y motor gráfico 2D — Kitchi Studio

Recursos gráficos, orden de capas y contrato entre diseño y desarrollo · Versión 1.1 · 28 de octubre de 2026

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

`assets/catalog.json` es la fuente de verdad del catálogo; el backend la valida contra la tabla `catalog_options` ([04_DATA_MODEL.md](04_DATA_MODEL.md)).

## Orden de composición

El orden debe ser explícito. Orden inicial posible:

1. Cuerpo y cola.
2. Pelaje y marcas.
3. Parte inferior.
4. Parte superior.
5. Cabello posterior.
6. Cabeza y rasgos faciales.
7. Cabello frontal.
8. Accesorios.
9. Elementos gráficos del sticker.

El orden definitivo dependerá de las ilustraciones. Si todas las prendas están diseñadas como capas completas, hay que evitar duplicar partes del cuerpo o crear huecos entre piezas.

## Contrato entre diseño y desarrollo

La diseñadora no entrega imágenes aisladas sin especificaciones. Desde la primera semana el equipo acuerda:

- [ ] Un lienzo y una resolución base comunes.
- [ ] El centro de referencia y las coordenadas de cada capa.
- [ ] Un sistema coherente de nombres de archivos.
- [ ] Una convención de transparencia.
- [ ] Reglas de superposición.
- [ ] Una lista de recursos obligatorios para el primer paquete.
- [ ] Una hoja de control de recursos aprobados y pendientes.

**Criterio de la primera entrega gráfica:** debe incluir un personaje completo que pueda componerse técnicamente. Es preferible un gato completo con pocas opciones que seis categorías incompletas.

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
- **Consistencia visual:** las 18 opciones comparten proporciones, paleta y estilo; no se mezclan ilustraciones incompatibles.
- **Estados completos:** cada pantalla debe tener estado de carga, vacío, error y éxito. Un fallo visible y comprensible cuenta para el criterio 2.
- **Feedback inmediato:** al cambiar una categoría, el personaje se actualiza; al generar, se muestra progreso; al descargar, se confirma el resultado.
- **Accesibilidad básica:** contraste suficiente, textos legibles, controles con etiquetas y navegación clara.
- **Recursos originales o con licencia:** no se copian personajes, interfaces ni stickers de terceros sin permiso. La autoría y licencia se registran en `assets/catalog.json`.
- **Evidencias visuales:** capturas del editor, del paquete y del hub para el README y la sustentación.
- **Commits de la diseñadora:** los recursos, la guía visual y los ajustes de diseño se registran con commits propios y descriptivos.

## Estado

- Guía visual y proporciones: **pendiente** de aprobación (tarea P06, fecha objetivo 31 de octubre).
- Previsualización provisional: el editor usa la paleta del catálogo local y etiquetas de
  color para cada pieza; no pretende ser el arte final ni reemplaza los assets (9 nov).
- Primer gato componible: **pendiente** (tarea P04 / día 2 del plan de 72 horas).
- Formato definitivo de recursos y poses: decisión pendiente con fecha 2 de noviembre ([01_MASTER_PLAN.md](01_MASTER_PLAN.md)).
- Capturas para README y sustentación: **pendiente** (tarea P31/P37).

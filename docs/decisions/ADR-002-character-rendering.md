# ADR-002 — Renderizado de personajes 2D por capas con Pillow

- **Estado:** Aceptado (propuesta del plan maestro; pendiente de validación con el primer gato componible, tarea P04)
- **Fecha:** 2026-10-26
- **Responsables:** Integrante C + diseñadora gráfica

## Contexto y problema

El editor debe permitir combinar seis campos de personalización con tres opciones cada uno (3⁶ = 729 combinaciones teóricas) sin producir 729 ilustraciones, manteniendo coherencia visual y produciendo PNG con transparencia a partir de una configuración persistente del personaje.

## Alternativas evaluadas

1. **Una imagen pre-renderizada por combinación** — descartada: 729 imágenes inalcanzables con presupuesto cero y cualquier cambio gráfico obligaría a regenerarlas todas.
2. **Composición 2D por capas con Pillow** (elegida) — almacenar una configuración del personaje y reconstruir su apariencia combinando recursos compatibles en un orden explícito.
3. **Renderizado en el cliente (canvas/SVG) sin motor en backend** — descartada para el MVP: la generación de stickers, su validación (dimensiones, canal alfa) y las evidencias de rendimiento/paralelismo requieren un motor en Python.
4. **Modelos o assets generados por IA en tiempo real** — descartada: inconsistencia entre resultados y dependencia del proveedor.

## Decisión

El personaje se define por un documento de configuración JSON validado contra el catálogo de recursos ([04_DATA_MODEL.md](../04_DATA_MODEL.md)) y el motor compone las capas con Pillow en el orden explícito definido en [06_DESIGN_SYSTEM.md](06_DESIGN_SYSTEM.md). La función principal es determinista. Exportación: PNG RGBA, 512×512, sRGB cuando sea posible.

## Justificación

- Con 18 opciones conceptuales el catálogo cubre las 729 combinaciones.
- Es la base de los criterios AC-01 a AC-04 y del caso de uso de multiprocesamiento/paralelismo (composición intensiva en CPU).
- Permite que la IA sea opcional: el flujo manual funciona sin ella.

## Consecuencias y riesgos

- **Riesgo:** inconsistencia de ilustraciones (anclajes, transparencias) → mitigado con el contrato diseño–desarrollo y la hoja de control de recursos ([06_DESIGN_SYSTEM.md](06_DESIGN_SYSTEM.md)).
- **Riesgo:** retrasos en las capas → primera entrega: un gato completo con pocas opciones antes que seis categorías incompletas.
- El orden de capas definitivo y las claves del esquema pueden cambiar según las ilustraciones; la compatibilidad de prendas/accesorios debe validarse con pruebas de composición.

## Documentos afectados

[06_DESIGN_SYSTEM.md](../06_DESIGN_SYSTEM.md) · [04_DATA_MODEL.md](../04_DATA_MODEL.md) · [02_REQUIREMENTS.md](../02_REQUIREMENTS.md)

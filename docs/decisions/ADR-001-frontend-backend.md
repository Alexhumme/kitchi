# ADR-001 — Separación Flet (interfaz) / Django REST Framework (API)

- **Estado:** Aceptado (propuesta del plan maestro; pendiente de validación técnica de la semana 1, tareas P01–P02)
- **Fecha:** 2026-10-26
- **Responsables:** Integrantes A y B

## Contexto y problema

El equipo debe decidir cómo repartir interfaz, lógica de negocio y persistencia entre las tecnologías elegidas para el curso (Python), con presupuesto cero y cuatro semanas de desarrollo. Existe el riesgo de repartir la lógica entre dos sistemas o crear dos backends.

## Alternativas evaluadas

1. **Aplicación monolítica Django con templates** — descartada: el plan prioriza una experiencia tipo "juego de vestir personajes" y Flet es la interfaz propuesta para web móvil.
2. **Flet como interfaz + Django REST Framework como API** (elegida) — capa de presentación en Flet, validación/autorización/reglas de negocio en Django.
3. **Flet con lógica de negocio embebida, Django solo para datos** — descartada: duplicaría lógica entre cliente y servidor y debilitaría los controles de acceso.
4. **Microservicios o backend adicional** — descartado: complejidad injustificable para el MVP.

## Decisión

Flet es la interfaz del prototipo web y Django REST Framework es la API del sistema, con MySQL como persistencia relacional y almacenamiento de archivos en el sistema de archivos local. Un solo backend.

## Justificación

- Mantiene responsabilidades claras (capa 1 interfaz / capa 2 API / capa 3 motor de generación).
- La validación y autorización residen en el backend, requisito de las reglas de acceso y de AC-05/AC-14.
- Se apoya en librerías conocidas y evita colas de mensajes o servidores de tareas en la primera versión.
- El PDF del curso no impone un stack concreto; Flet + DRF cumple el requisito de aplicación real con interfaz y API ([ADR-004](ADR-004-academic-requirements.md)).

## Consecuencias y riesgos

- **Riesgo:** que la versión elegida de Flet no sirva el prototipo web móvil como se espera o no pueda comunicarse con la API → se valida en la semana 1 (condiciones de [01_MASTER_PLAN.md](../01_MASTER_PLAN.md)).
- **Riesgo:**frontend y backend en paralelo sin contratos → mitigado acordando contratos en la semana 1 ([05_API_CONTRACTS.md](../05_API_CONTRACTS.md)).
- El mecanismo exacto de autenticación entre Flet y Django queda como decisión pendiente propia (sesión 18); cuando se cierre, actualizar este ADR o crear uno nuevo.

## Documentos afectados

[03_ARCHITECTURE.md](../03_ARCHITECTURE.md) · [01_MASTER_PLAN.md](../01_MASTER_PLAN.md)

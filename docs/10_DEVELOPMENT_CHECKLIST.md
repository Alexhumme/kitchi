# 10 · Checklist de desarrollo — Kitchi Studio

Tablero de seguimiento del proyecto · Versión 1.0

> Este archivo es el tablero de seguimiento del proyecto. Cada tarea tiene identificador, responsable, dependencia, estado y criterio de aceptación. Formato de casilla: `- [ ]` pendiente, `- [~]` en progreso, `- [x]` terminada con evidencia.

**Regla:** no se deben marcar tareas como terminadas únicamente porque el código se haya escrito. Una tarea solo está terminada cuando satisface sus criterios de aceptación, las pruebas pertinentes pasan y la documentación afectada queda actualizada ([AGENTS.md](../AGENTS.md)).

## Semana 1 — Fundamentos

- [ ] **P01** — Confirmar la rúbrica académica. *Responsable: todo el equipo · Dependencia: ninguna · Criterio: rúbrica transcrita en [08_CONCURRENCY_AND_PARALLELISM.md](08_CONCURRENCY_AND_PARALLELISM.md) y las preguntas de [01_MASTER_PLAN.md](01_MASTER_PLAN.md) respondidas.*
- [ ] **P02** — Validar Flet, Django REST Framework y MySQL. *Responsable: A + B · Dependencia: P01 · Criterio: prototipo mínimo Flet ↔ API ↔ MySQL funcionando; registro en `docs/reports/`.*
- [ ] **P03** — Definir contratos iniciales de la API. *Responsable: A + B · Dependencia: P02 · Criterio: tabla de endpoints definitiva en [05_API_CONTRACTS.md](05_API_CONTRACTS.md) y contratos en `shared/contracts/`.*
- [ ] **P04** — Probar composición de un gato con capas. *Responsable: C · Dependencia: capas iniciales de la diseñadora · Criterio: un gato visible compuesto con Pillow; tiempos registrados.*
- [ ] **P05** — Evaluar una opción real de IA. *Responsable: C · Dependencia: ninguna · Criterio: las 7 preguntas de [07_AI_INTEGRATION.md](07_AI_INTEGRATION.md#criterio-para-elegir-el-modelo) respondidas y ADR-003 actualizado.*
- [ ] **P06** — Aprobar guía de ilustraciones y poses. *Responsable: diseñadora + C · Dependencia: ninguna · Criterio: contrato de diseño de [06_DESIGN_SYSTEM.md](06_DESIGN_SYSTEM.md) con los 7 puntos acordados.*
- [x] **P07** — Crear repositorio y reglas de integración. *Responsable: todo el equipo · Dependencia: ninguna · Criterio: estructura documental, `AGENTS.md` y reglas de ramas/revisiones establecidas.* (hecho con esta entrega; falta inicializar Git y el repositorio remoto)

## Semana 2 — Editor y persistencia

- [ ] **P08** — Implementar catálogo de recursos. *Responsable: B + diseñadora · Dependencia: P06 · Criterio: `catalog.json` + tabla `catalog_options` coherentes y servidos por `/api/catalog/`.*
- [ ] **P09** — Implementar configuración de personajes. *Responsable: C · Dependencia: P08 · Criterio: documento de configuración validado contra catálogo (schema_version).* 
- [ ] **P10** — Implementar editor manual. *Responsable: A · Dependencia: P08, P09 · Criterio: AC-01 y AC-02.*
- [ ] **P11** — Crear modelos y migraciones. *Responsable: B · Dependencia: P08 · Criterio: esquema de [04_DATA_MODEL.md](04_DATA_MODEL.md) aplicado vía migraciones de Django.*
- [ ] **P12** — Implementar registro e inicio de sesión. *Responsable: B + A · Dependencia: P03, P11 · Criterio: AC-06.*

## Semana 3 — Generación e IA

- [ ] **P13** — Componer las seis poses. *Responsable: C · Dependencia: P09 · Criterio: seis poses renderizadas desde configuración válida.*
- [ ] **P14** — Exportar PNG con transparencia. *Responsable: C · Dependencia: P13 · Criterio: AC-03 y AC-04.*
- [ ] **P15** — Implementar seguimiento de trabajos. *Responsable: B + C · Dependencia: P11, P13 · Criterio: ciclo `pending → running → completed/failed` consultable por polling.*
- [ ] **P16** — Integrar y probar el flujo de IA. *Responsable: C · Dependencia: P05 · Criterio: AC-08 o contingencia documentada.*
- [ ] **P17** — Añadir gestión de errores y reintentos. *Responsable: B + A · Dependencia: P15, P16 · Criterio: códigos de error de [05_API_CONTRACTS.md](05_API_CONTRACTS.md) y reintentos de IA funcionales.*

## Semana 4 — Hub y programación avanzada

- [ ] **P18** — Implementar publicación y galería. *Responsable: A + B · Dependencia: P12 · Criterio: AC-07 (primera parte).*
- [ ] **P19** — Implementar copia de creaciones. *Responsable: A + B · Dependencia: P18 · Criterio: AC-07 completo; la copia no altera el original.*
- [ ] **P20** — Demostrar concurrencia. *Responsable: C · Dependencia: P16 · Criterio: AC-09 con operaciones reales (no `sleep` artificial).*
- [ ] **P21** — Demostrar multiprocesamiento. *Responsable: C · Dependencia: P13 · Criterio: AC-10; procesos identificados en logs.*
- [ ] **P22** — Ejecutar benchmark de paralelismo. *Responsable: C · Dependencia: P21 · Criterio: AC-11; informe reproducible con fórmula de aceleración.*
- [ ] **P23** — Completar pruebas de permisos y límites. *Responsable: B · Dependencia: P12, P18 · Criterio: AC-05 y tabla de pruebas de seguridad de [09_TEST_PLAN.md](09_TEST_PLAN.md).*

## Semana 5 — Integración y entrega

- [ ] **P24** — Ejecutar pruebas de aceptación. *Responsable: todo el equipo · Dependencia: P10–P23 · Criterio: escenario principal de 9 pasos completado sin editar la BD.*
- [ ] **P25** — Corregir errores críticos. *Responsable: según componente · Dependencia: P24 · Criterio: sin fallos que bloqueen el flujo integral.*
- [ ] **P26** — Preparar datos de demostración. *Responsable: A + B · Dependencia: P24 · Criterio: `scripts/seed_demo_data.py` con cuentas y personajes listos.*
- [ ] **P27** — Documentar resultados de rendimiento. *Responsable: C · Dependencia: P22 · Criterio: informe con equipo, versión de Python, tamaños, repeticiones y metodología.*
- [ ] **P28** — Ensayar demostración visual y técnica. *Responsable: todo el equipo · Dependencia: P26, P27 · Criterio: [11_DEMO_SCRIPT.md](11_DEMO_SCRIPT.md) ejecutado de corrido en 8–12 minutos.*
- [ ] **P29** — Verificar instalación desde un clon limpio. *Responsable: un integrante distinto del configurador · Dependencia: P25 · Criterio: AC-13 registrado en `docs/reports/`.*
- [ ] **P30** — Congelar versión de entrega. *Responsable: responsable de integración · Dependencia: todas · Criterio: etiqueta de versión, dependencias fijadas, docs actualizados (AC-12).*

## Plantilla para añadir subtareas

```
- [ ] **PXX** — Título.
  - Responsable: ...
  - Dependencia: PX, PY
  - Criterio de aceptación: AC-XX / descripción verificable
  - Evidencia: enlace a prueba, log o captura en docs/reports/
```

> El plan maestro original contiene las tareas sin metadatos; esta versión añade responsable, dependencia y criterio para cumplir la indicación de la sección 10.3 del plan maestro. Actualizar si la rúbrica del profesor (P01) cambia el alcance.

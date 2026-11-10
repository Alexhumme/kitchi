# 10 · Checklist de desarrollo — Kitchi Studio

Tablero de seguimiento del proyecto · Versión 1.1 · 28 de octubre de 2026

> Este archivo es el tablero de seguimiento del proyecto. Cada tarea tiene identificador, responsable, dependencia, estado y criterio de aceptación. Formato de casilla: `- [ ]` pendiente, `- [~]` en progreso, `- [x]` terminada con evidencia.
>
> **Regla:** no se deben marcar tareas como terminadas únicamente porque el código se haya escrito. Una tarea solo está terminada cuando satisface sus criterios de aceptación, las pruebas pertinentes pasan y la documentación afectada queda actualizada ([AGENTS.md](../AGENTS.md)). La auditoría final está en [`13_CUMPLIMIENTO_ACADEMICO.md`](13_CUMPLIMIENTO_ACADEMICO.md).

## Semana 1 — Fundamentos (28 oct – 3 nov)

- [x] **P01** — Transcribir y analizar la rúbrica académica. *Responsable: todo el equipo · Dependencia: ninguna · Criterio: rúbrica en [`reports/rubric.md`](reports/rubric.md) y requisitos en [`13_CUMPLIMIENTO_ACADEMICO.md`](13_CUMPLIMIENTO_ACADEMICO.md).*
- [~] **P02** — Validar Flet, Django REST Framework, MySQL, Pillow y Swagger. *Responsable: A + B · Dependencia: P01 · Criterio: prototipo mínimo Flet ↔ API ↔ MySQL funcionando y `/api/docs/` disponible; registro en `docs/reports/week1-validation.md`.* **Backend validado (4 nov):** Django ↔ MySQL, migraciones desde cero, Swagger y esquema versionado. **Flet integrado (9 nov):** cliente HTTP, catálogo/poses y cuentas consumidos por las pantallas; 34 pruebas de frontend en verde y smoke test de todas las pantallas. Falta la prueba manual completa en navegador con backend real y el motor Pillow. Evidencia en [`reports/frontend-integration.md`](reports/frontend-integration.md).
- [~] **P03** — Definir contratos iniciales de la API. *Responsable: A + B · Dependencia: P02 · Criterio: tabla de endpoints definitiva en [05_API_CONTRACTS.md](05_API_CONTRACTS.md) y contratos en `shared/contracts/`.* **Avance (4 nov):** rutas de cuentas, catálogo, poses y gatos fijadas; autenticación por token y RBAC acordadas en [ADR-005](decisions/ADR-005-autenticacion-y-rbac.md); `shared/contracts/openapi.yaml` publicado. Faltan las rutas de paquetes, IA y comunidad.
- [ ] **P04** — Probar composición de un gato con capas. *Responsable: C · Dependencia: capas iniciales de la diseñadora · Criterio: un gato visible compuesto con Pillow; tiempos registrados.*
- [ ] **P05** — Evaluar una opción real de IA. *Responsable: C · Dependencia: ninguna · Criterio: las 7 preguntas de [07_AI_INTEGRATION.md](07_AI_INTEGRATION.md#criterio-para-elegir-el-modelo) respondidas y ADR-003 actualizado.*
- [ ] **P06** — Aprobar guía de ilustraciones y poses. *Responsable: diseñadora + C · Dependencia: ninguna · Criterio: contrato de diseño de [06_DESIGN_SYSTEM.md](06_DESIGN_SYSTEM.md) con los 7 puntos acordados.*
- [~] **P07** — Crear repositorio y reglas de integración. *Responsable: todo el equipo · Dependencia: ninguna · Criterio: estructura documental, `AGENTS.md`, repositorio local y remoto; falta verificar visibilidad pública y permisos.*
- [~] **P31** — Completar README académico. *Responsable: A · Dependencia: P01 · Criterio: nombre, problema, funciones, stack, instalación, uso de IA, integrantes y enlace; faltan nombres e instalación verificada.* **Avance (9 nov):** README actualizado con el estado real del frontend, instalación de Flet, sembrado del catálogo, comandos de prueba y uso de IA; faltan la verificación desde clon limpio y completar roles/nombres definitivos.
- [x] **P32** — Crear `requirements.txt` con versiones fijadas. *Responsable: B + A · Dependencia: P02 · Criterio: instalación reproducible y sin versiones flotantes.* **Backend hecho (4 nov):** `backend/requirements.txt` con 10 versiones fijadas en Python 3.14.7. **Frontend (9 nov):** `frontend/pyproject.toml` fija `flet[web]==1.1.2` y `requires-python >=3.11`; se instaló y ejecutó con Python 3.11.6. Falta la verificación en clon limpio (P29).
- [x] **P33** — Publicar Swagger/OpenAPI. *Responsable: B · Dependencia: P03 · Criterio: `/api/schema/` y `/api/docs/` funcionando con drf-spectacular.* **Hecho (4 nov):** ambos responden 200, 9 endpoints, 0 errores y 0 advertencias; esquema en `shared/contracts/openapi.yaml`. Evidencia en `docs/reports/week1-validation.md`.
- [ ] **P34** — Establecer y auditar la política de commits. *Responsable: integración · Dependencia: P07 · Criterio: mínimo 5 commits descriptivos por integrante y sin secretos; evidencia en `reports/commits-audit.md`.*
- [x] **P35** — Crear la guía viva de la plataforma. *Responsable: todo el equipo · Dependencia: P01 · Criterio: [`12_GUIA_PLATAFORMA.md`](12_GUIA_PLATAFORMA.md) con esqueleto y reglas de actualización.*
- [~] **P36** — Actualizar la guía viva por incremento. *Responsable: quien implementa · Dependencia: cada tarea funcional · Criterio: la guía refleja el flujo real, sin funciones inventadas.* **Avance (9 nov):** secciones 1–5, 7, 12 y registro actualizadas con la interfaz Flet real, el modo invitado/cuenta, placeholders y limitaciones vigentes.

## Semana 2 — Editor y persistencia (4 – 10 nov)

- [~] **P08** — Implementar catálogo de recursos. *Responsable: B + diseñadora · Dependencia: P06 · Criterio: `catalog.json` + tabla `catalog_options` coherentes y servidos por `/api/catalog/`.* **Media:** endpoint y tabla listos y la consola `/admin/` ya permite cargar y activar opciones y poses (4 nov). **Sembrado provisional (9 nov):** `scripts/seed_catalog.py` cargó 18 opciones y 6 poses con rutas de placeholder; `/api/catalog/` y `/api/poses/` ya devuelven datos. Sigue pendiente el `catalog.json`/assets reales de la diseñadora y su coherencia con la tabla.
- [ ] **P09** — Implementar configuración de personajes. *Responsable: C · Dependencia: P08 · Criterio: documento de configuración validado contra catálogo (schema_version).*
- [~] **P10** — Implementar editor manual. *Responsable: A · Dependencia: P08, P09 · Criterio: AC-01 y AC-02.* **Avance (9 nov):** editor completo con seis categorías, tres opciones cada una, previsualización en tiempo real con placeholders de color, guardado en cuenta o invitado, edición, eliminación y deshacer; 34 pruebas en verde. Falta sustituir los placeholders por los assets finales (P06) y probarlo manualmente en navegador.
- [x] **P11** — Crear modelos y migraciones. *Responsable: B · Dependencia: P08 · Criterio: esquema de [04_DATA_MODEL.md](04_DATA_MODEL.md) aplicado vía migraciones de Django.* **Hecho (4 nov):** 6 apps con sus modelos, índices, restricciones y estados validados; 19 tablas aplicadas en MySQL 8.0.45. Evidencia: `python manage.py migrate` y `pytest` (30 pruebas).
- [~] **P12** — Implementar registro e inicio de sesión. *Responsable: B + A · Dependencia: P03, P11 · Criterio: AC-06.* **Backend hecho (4 nov):** registro, login, logout y `me` con token de Django y roles RBAC ([ADR-005](decisions/ADR-005-autenticacion-y-rbac.md)). **Frontend (9 nov):** pantallas de login/registro, sesión persistida, logout, perfil real y migración de gatos de invitado a la cuenta. Falta verificarlo manualmente en navegador y cubrir el caso de token expirado en vivo.
- [~] **P39** — Implementar manejo de errores visible. *Responsable: A + B · Dependencia: P10, P12 · Criterio: estados de carga, vacío, error y éxito en las pantallas principales.* **Avance (9 nov):** login/registro muestran errores inline y estado de carga; guardado/eliminación usan SnackBar; perfil, hub y Mis gatos distinguen API conectada, modo local y endpoint pendiente. Falta cubrir todos los estados de stickers/IA cuando existan sus endpoints.

## Semana 3 — Stickers, IA y comunidad (11 – 17 nov)

- [ ] **P13** — Componer las seis poses. *Responsable: C · Dependencia: P09 · Criterio: seis poses renderizadas desde configuración válida.*
- [ ] **P14** — Exportar PNG con transparencia. *Responsable: C · Dependencia: P13 · Criterio: AC-03 y AC-04.*
- [ ] **P15** — Implementar seguimiento de trabajos. *Responsable: B + C · Dependencia: P11, P13 · Criterio: ciclo `pending → running → completed/failed` consultable por polling.*
- [ ] **P16** — Integrar y probar el flujo de IA. *Responsable: C · Dependencia: P05 · Criterio: AC-08 o contingencia documentada.*
- [ ] **P17** — Añadir gestión de errores y reintentos. *Responsable: B + A · Dependencia: P15, P16 · Criterio: códigos de error de [05_API_CONTRACTS.md](05_API_CONTRACTS.md) y reintentos de IA funcionales.*
- [ ] **P18** — Implementar publicación y galería. *Responsable: A + B · Dependencia: P12 · Criterio: AC-07 (primera parte).*
- [ ] **P19** — Implementar copia de creaciones. *Responsable: A + B · Dependencia: P18 · Criterio: AC-07 completo; la copia no altera el original.*
- [ ] **P20** — Demostrar concurrencia. *Responsable: C · Dependencia: P16 · Criterio: AC-09 con operaciones reales (no `sleep` artificial).*
- [ ] **P21** — Demostrar multiprocesamiento. *Responsable: C · Dependencia: P13 · Criterio: AC-10; procesos identificados en logs.*
- [ ] **P22** — Ejecutar benchmark de paralelismo. *Responsable: C · Dependencia: P21 · Criterio: AC-11; informe reproducible con fórmula de aceleración.*
- [ ] **P23** — Completar pruebas de permisos y límites. *Responsable: B · Dependencia: P12, P18 · Criterio: AC-05 y tabla de pruebas de seguridad de [09_TEST_PLAN.md](09_TEST_PLAN.md).*

## Semana 4 — Integración, documentación y entrega (18 – 25 nov)

- [ ] **P24** — Ejecutar pruebas de aceptación. *Responsable: todo el equipo · Dependencia: P10–P23 · Criterio: escenario principal de 13 pasos completado sin editar la BD.*
- [ ] **P25** — Corregir errores críticos y congelar alcance. *Responsable: según componente · Dependencia: P24 · Criterio: sin fallos que bloqueen el flujo integral; congelación el 20 de noviembre.*
- [ ] **P26** — Preparar datos de demostración. *Responsable: A + B · Dependencia: P24 · Criterio: `scripts/seed_demo_data.py` idempotente con cuentas y personajes listos.*
- [ ] **P27** — Documentar resultados de rendimiento. *Responsable: C · Dependencia: P22 · Criterio: informe con equipo, versión de Python, tamaños, repeticiones y metodología.*
- [ ] **P28** — Ensayar demostración visual y técnica. *Responsable: todo el equipo · Dependencia: P26, P27 · Criterio: [11_DEMO_SCRIPT.md](11_DEMO_SCRIPT.md) ejecutado en 10 minutos.*
- [ ] **P29** — Verificar instalación desde un clon limpio. *Responsable: un integrante distinto del configurador · Dependencia: P25 · Criterio: AC-13 registrado en `docs/reports/clean-install.md`.*
- [ ] **P30** — Congelar versión de entrega. *Responsable: responsable de integración · Dependencia: todas · Criterio: etiqueta de versión, dependencias fijadas, docs actualizados (AC-12) y enlace enviado antes del plazo.*
- [ ] **P37** — Ensayar la defensa individual. *Responsable: todo el equipo · Dependencia: P28 · Criterio: cada integrante explica un módulo ajeno y navega el código; registro en `reports/defense-rehearsal.md`.*
- [ ] **P38** — Verificar README y uso de IA. *Responsable: A · Dependencia: P31 · Criterio: todas las secciones obligatorias y herramientas declaradas; evidencia en `reports/readme-check.md`.*
- [ ] **P40** — Ejecutar la auditoría académica final. *Responsable: integración · Dependencia: P29–P38 · Criterio: [`reports/academic-audit.md`](reports/academic-audit.md) completo y sin pendientes bloqueantes.*

## Política de commits

- Una rama por funcionalidad; commits pequeños y descriptivos.
- Mínimo **5 commits por integrante**, incluida la diseñadora. No se aceptan commits masivos de una sola persona.
- Mensajes en imperativo y con contexto: `feat(editor): agregar selector de pelaje`, `docs(guia): documentar flujo de stickers`.
- No se versionan `.env`, `__pycache__`, bases locales, capturas privadas ni resultados temporales.
- Antes de la entrega: `git shortlog -sne --all`, revisión de secretos y verificación de que el repositorio es público.

## Plantilla para añadir subtareas

```
- [ ] **PXX** — Título.
  - Responsable: ...
  - Dependencia: PX, PY
  - Criterio de aceptación: AC-XX / descripción verificable
  - Evidencia: enlace a prueba, log o captura en docs/reports/
```

> El plan maestro original contiene las tareas sin metadatos; esta versión añade responsable, dependencia, criterio y las tareas académicas P31–P40. Actualizar si el docente responde las preguntas pendientes de [01_MASTER_PLAN.md](01_MASTER_PLAN.md).

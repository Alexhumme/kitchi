# 01 · Plan maestro — Kitchi Studio

Plan rector del proyecto · Versión 1.1 · 28 de octubre de 2026

> Resumen operativo del plan maestro. El documento original completo se conserva como referencia histórica en [`project.md`](../project.md); la planificación vigente es este archivo. La rúbrica y los entregables del curso están en [`13_CUMPLIMIENTO_ACADEMICO.md`](13_CUMPLIMIENTO_ACADEMICO.md).

## Cambio de calendario

El plan original asumía cinco semanas. La fecha límite del curso es el **miércoles 25 de noviembre de 2026 a las 12:00 m.**, por lo que el proyecto se comprime a **cuatro semanas**:

| Aspecto | Plan original | Plan vigente |
| --- | --- | --- |
| Duración | 5 semanas | 4 semanas (28 oct – 25 nov) |
| Entrega | Demostración visual y técnica | Repositorio + sustentación de 10 minutos |
| Cierre | Semana 5 | Entrega interna el martes 24 de noviembre; envío antes del mediodía del 25 |
| Concurrencia / IA | Requisitos centrales | Diferenciadores de calidad técnica, subordinados a las 3 funcionalidades mínimas |

La decisión está registrada en [ADR-004](decisions/ADR-004-academic-requirements.md).

## Estrategia general

- Enfoque 2D por capas: el motor combina recursos compatibles; no se producen las 3⁶ = 729 combinaciones como imágenes independientes, sino un catálogo inicial de 18 opciones conceptuales (3 por cada uno de los 6 campos).
- Comenzar por el motor gráfico y los contratos de API.
- Validar la IA en la primera semana, antes de comprometerse con un modelo concreto.
- Priorizar las **tres funcionalidades completas** que exige la rúbrica: editor de personajes, generación/descarga de stickers y cuenta + comunidad. La IA y el benchmark son diferenciadores.
- Reservar la última semana para estabilización, documentación, instalación limpia y ensayo de la defensa; no para funcionalidades nuevas.
- Resultado funcional desde la primera semana, para descubrir los riesgos técnicos temprano.

## Cronograma de cuatro semanas

### Semana 1 — Validación y cimientos (28 oct – 3 nov)

Objetivo: eliminar las incertidumbres que podrían bloquear el MVP y dejar lista la base académica.

- Transcribir la rúbrica y ajustar el alcance ([P01](10_DEVELOPMENT_CHECKLIST.md)).
- Crear repositorio público, estructura documental, README inicial y reglas de agentes.
- Validar Flet Web móvil, Django REST Framework, MySQL, Pillow y Swagger.
- Componer un gato con varias capas reales.
- Comparar opciones de IA con una prueba mínima.
- Aprobar contratos iniciales de API y catálogo gráfico.
- Preparar un ejemplo de benchmark de procesamiento.
- Definir la política de commits y la guía viva de la plataforma.

**Hito:** un gato visible desde recursos 2D, una decisión fundamentada sobre IA y la base académica documentada.

### Semana 2 — Editor y persistencia (4 – 10 nov)

- Implementar navegación principal.
- Implementar selectores de las seis categorías.
- Crear modelos y migraciones.
- Implementar registro e inicio de sesión.
- Guardar y recuperar configuraciones de gatos.
- Aplicar el límite de tres gatos.
- Publicar Swagger/OpenAPI y los primeros contratos en `shared/contracts/`.
- Completar los nombres de los integrantes en el README.

**Hito:** un usuario puede personalizar un gato, guardarlo y recuperarlo; la API está documentada.

### Semana 3 — Stickers, IA y comunidad (11 – 17 nov)

- Implementar las seis poses.
- Componer imágenes mediante Pillow.
- Exportar PNG transparentes.
- Implementar el registro y seguimiento de trabajos.
- Integrar la IA elegida.
- Implementar errores, límites y reintentos.
- Implementar publicación, exploración y copia de creaciones.
- Demostrar concurrencia y multiprocesamiento con operaciones reales.
- Ejecutar el benchmark secuencial y paralelo.
- Verificar permisos, límites y privacidad.

**Hito:** el flujo integral funciona y existen evidencias técnicas de los conceptos avanzados.

### Semana 4 — Pruebas, documentación y entrega (18 – 25 nov)

- Ejecutar pruebas unitarias, de integración y de aceptación.
- Corregir errores críticos y congelar funcionalidades el **viernes 20 de noviembre**.
- Verificar que el proyecto se instala desde un clon limpio.
- Preparar datos de demostración.
- Documentar resultados de rendimiento y auditoría académica.
- Actualizar la guía viva de la plataforma y el README.
- Ensayar la defensa de 10 minutos al menos dos veces.
- Congelar versiones y etiquetar la entrega.
- **Entrega interna:** martes 24 de noviembre a las 18:00.
- **Fecha límite:** miércoles 25 de noviembre a las 12:00 m.

**Hito:** prototipo demostrable, reproducible, documentado y defendible individualmente.

## Dependencias críticas

1. El editor no puede finalizarse sin una convención de recursos gráficos.
2. El backend no puede integrarse con el frontend sin contratos de API.
3. El generador de stickers debe funcionar antes de incorporar paralelismo.
4. La guía viva y el guion de la demo deben actualizarse desde la semana 2, no al final.
5. El README debe completarse antes de la entrega interna, no durante la sustentación.
6. La prueba de IA se realizará en la primera semana. No se dejará para después de terminar el editor.

## Regla para recuperar retrasos

- Si al final de la **semana 1** no hay un gato componible o una decisión de IA, se congela el alcance de IA y se continúa con el editor manual.
- Si al final de la **semana 2** el editor y la persistencia todavía no funcionan → se congelan las funcionalidades P1.
- Si al final de la **semana 3** la IA no está integrada → se documenta el motivo y se aplica el plan de contingencia ([07_AI_INTEGRATION.md](07_AI_INTEGRATION.md)), sin comprometer la generación manual de stickers ni el hub.
- Si al final de la **semana 3** el benchmark de paralelismo no está listo → se presenta como evidencia opcional y se prioriza la demo funcional.
- La última semana no se usa para funcionalidades nuevas. Solo estabilización, documentación, ensayo y entrega.

## Condiciones técnicas que deben verificarse en la semana 1

Antes de desarrollar todas las pantallas, validar:

- Que la versión elegida de Flet permita servir el prototipo web móvil como se espera.
- Que el cliente Flet pueda comunicarse correctamente con la API de Django.
- Que la autenticación elegida funcione con el cliente y con las peticiones de descarga.
- Que Pillow pueda componer los recursos gráficos en el formato requerido.
- Que el método de IA elegido permita ejecutar una prueba real sin pago.
- Que MySQL sea instalable y reproducible en los equipos del equipo.
- Que drf-spectacular genere el esquema OpenAPI y la interfaz Swagger.
- Que la herramienta de desarrollo y las versiones de Python sean compatibles.

Las versiones exactas se fijan en los archivos de dependencias una vez comprobadas. No usar versiones flotantes ni actualizar dependencias a mitad del proyecto sin razón concreta.

## Decisiones pendientes y protocolo de aprobación

| Prioridad | Decisión pendiente | Responsable sugerido | Fecha límite |
| --- | --- | --- | --- |
| Crítica | Prueba real de IA sin coste | Integrante C | 31 oct |
| Crítica | Compatibilidad del prototipo web con Flet | Integrante A | 30 oct |
| Crítica | Primer gato completo y contrato de capas | Diseñadora + C | 31 oct |
| Alta | Contratos iniciales de API y Swagger | A + B | 1 nov |
| Alta | Esquema inicial de datos y autenticación | Integrante B | 2 nov |
| Alta | Formato definitivo de recursos y poses | Diseñadora + C | 2 nov |
| Alta | Mecanismo de autenticación entre Flet y Django | A + B | 3 nov |
| Media | Persistencia de invitados y recuperación de sesiones | A + B | Semana 2 |
| Media | Comportamiento visual del plan premium simulado | A + diseñadora | Semana 2 |
| Media | Contingencia de base de datos si MySQL bloquea el clon limpio | B + integración | Semana 3 |

Estas fechas son objetivos internos, no garantías. Si una prueba crítica falla, se registra el problema y se toma una decisión explícita en [`decisions/`](decisions/) en vez de continuar suponiendo que se resolverá más adelante.

## Preguntas al profesor: respondidas y pendientes

El PDF del curso responde varias preguntas del plan original:

- **¿Se exige una tecnología concreta?** No. El PDF no impone arquitectura ni patrón de diseño; recomienda tecnologías web y de backend.
- **¿Se exige IA?** No. El uso de IA está permitido y puede integrarse en la app, pero no es obligatorio.
- **¿Cómo se califica?** Rúbrica de 5.0 con cinco criterios; ver [`reports/rubric.md`](reports/rubric.md).
- **¿Qué se entrega?** Repositorio Git público + README + sustentación de 10 minutos.
- **¿Cuántos integrantes?** De 2 a 4; el proyecto declara 4.
- **¿Hay requisitos de commits?** Sí: todos deben tener commits y se esperan al menos 5 descriptivos por integrante.
- **¿Se exige concurrencia o paralelismo?** No explícitamente. Se conservan como diferenciadores.

Preguntas que aún conviene confirmar con el docente (hasta el 18 de noviembre):

1. ¿La diseñadora cuenta como integrante para efectos de commits y sustentación?
2. ¿Se valora especialmente la concurrencia, el multiprocesamiento o el paralelismo aunque no estén en la rúbrica?
3. ¿La IA debe ser una inferencia real o se acepta una integración con contingencia documentada?
4. ¿Se permite MySQL o se prefiere SQLite/PostgreSQL para la demo?
5. ¿La entrega del enlace debe hacerse por correo o por el aula virtual?

Las respuestas se registran en [`reports/rubric.md`](reports/rubric.md) o en un ADR si cambian el alcance.

## Primeras 72 horas

### Día 1 — 28 de octubre: organización

- Transcribir la rúbrica y ajustar el plan. ✅
- Crear la guía viva de la plataforma y las reglas académicas. ✅
- Verificar el repositorio público, los permisos y la política de commits.
- Asignar responsables y establecer el mecanismo de revisión de cambios.
- Completar los nombres de los integrantes en el README.

### Día 2 — 29 de octubre: pruebas técnicas

- Crear una aplicación mínima con Flet.
- Crear una API mínima con Django REST Framework.
- Conectar Django a MySQL.
- Publicar `/api/schema/` y `/api/docs/`.
- Componer un gato con dos o tres capas.
- Registrar tiempos de composición.

### Día 3 — 30 de octubre: validación de riesgos

- Probar el servicio o modelo de IA.
- Evaluar el resultado gráfico.
- Verificar compatibilidad del entorno.
- Aprobar la primera guía de recursos.
- Registrar las decisiones técnicas definitivas en [`decisions/`](decisions/).

**Al finalizar:** repositorio que arranca, un primer recurso gráfico componible, una API conectada a la base de datos, Swagger funcionando y una decisión sustentada sobre la viabilidad de IA.

## Registro de riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
| --- | --- | --- | --- |
| Calendario de 4 semanas | Alta | Alto | Congelar alcance, priorizar 3 funcionalidades, ensayar desde la semana 3 |
| Flet no cumple web móvil | Media | Alto | Validación temprana; ADR si hay que cambiar de interfaz |
| MySQL difícil en clon limpio | Media | Medio | Documentar instalación; validar P29; ADR de contingencia |
| IA sin API gratuita | Alta | Medio | Contingencia documentada y flujo manual |
| Retraso gráfico | Media | Alto | Primer gato completo con pocas opciones antes que seis categorías incompletas |
| Un integrante no entiende el código | Media | Alto | Guía viva, revisión cruzada y ensayos individuales |
| Commits concentrados | Alta | Alto | Reparto semanal y auditoría en P34 |

## Definición final del éxito

El proyecto se mide por la coherencia del sistema completo, no por la cantidad de pantallas o tecnologías. Un buen MVP cumple seis condiciones:

1. **Producto:** el usuario puede crear un gato y obtener un paquete de stickers real.
2. **Diseño:** las combinaciones son personalizables pero pertenecen a un lenguaje visual reconocible.
3. **Arquitectura:** interfaz, API, base de datos, almacenamiento y motor de generación tienen responsabilidades claras.
4. **Rigor académico:** la IA, la concurrencia, el multiprocesamiento y el paralelismo se explican y demuestran con evidencias, sin inventar resultados.
5. **Reproducibilidad:** un integrante nuevo o un evaluador puede comprender el repositorio, instalar el proyecto y repetir las pruebas.
6. **Cumplimiento:** README completo, repositorio público, commits de todos, Swagger, tres funcionalidades y defensa individual preparada ([`13_CUMPLIMIENTO_ACADEMICO.md`](13_CUMPLIMIENTO_ACADEMICO.md)).

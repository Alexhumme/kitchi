# 00 · Visión general del proyecto — Kitchi Studio

Documento de producto · MVP académico · Versión 1.1 · 28 de octubre de 2026

> Este es el punto de entrada obligatorio para cualquier integrante o agente de programación. Léelo antes que cualquier otro documento. La fuente vigente de los requisitos académicos es el PDF del profesor y su resumen operativo en [`13_CUMPLIMIENTO_ACADEMICO.md`](13_CUMPLIMIENTO_ACADEMICO.md).

## Qué es Kitchi Studio

Nombre de trabajo, sujeto a validación de marca.

Aplicación web móvil para crear gatos chibi personalizados mediante composición de ilustraciones 2D por capas, generar paquetes de seis stickers descargables y compartibles, explorar o reutilizar personajes publicados por otros usuarios y transformar fotografías de referencia en representaciones felinas estilizadas con asistencia de IA.

**Regla central del proyecto:** construir un producto pequeño pero funcional, cuya arquitectura permita demostrar claramente los conceptos académicos, en lugar de intentar reproducir una aplicación comercial completa.

## Datos generales

| Aspecto | Valor |
| --- | --- |
| Curso | Programación Avanzada A1 — Universidad de La Guajira |
| Duración | 4 semanas (28 de octubre – 25 de noviembre de 2026) |
| Fecha límite | Miércoles 25 de noviembre de 2026, 12:00 m. (hora Colombia) |
| Entrega | Repositorio Git + sustentación presencial de 10 minutos |
| Equipo | 4 integrantes: 3 desarrollo + 1 diseñadora gráfica |
| Modalidad | Desarrollo local |
| Presupuesto | Cero |
| Paquete MVP | 6 stickers |
| Cliente | Web móvil |
| Arte | 2D por capas |
| Stack | Python · Flet Web · Django REST Framework · MySQL · Pillow |

## Objetivo general

Desarrollar un prototipo web móvil funcional que permita crear personajes felinos de estilo chibi mediante personalización gráfica manual o transformación asistida por IA, generar paquetes de seis stickers con expresiones y poses predefinidas, descargarlos y compartirlos, y explorar o reutilizar personajes publicados por otros usuarios, cumpliendo la rúbrica del curso.

## Objetivos específicos

1. Implementar un editor de personajes mediante composición de ilustraciones 2D por capas.
2. Desarrollar un flujo de transformación de fotografías en representaciones felinas estilizadas, sujeto a la viabilidad del modelo de IA elegido.
3. Generar seis imágenes PNG con fondo transparente a partir de una configuración persistente del personaje.
4. Implementar acceso como invitado, registro, inicio de sesión y límites del plan gratuito.
5. Crear un hub donde los usuarios registrados publiquen, exploren y copien creaciones.
6. Demostrar concurrencia, multiprocesamiento y paralelismo mediante operaciones reales, medibles y documentadas, como diferenciador de calidad técnica.
7. Mantener documentación técnica, de producto y de sustentación suficiente para continuar el trabajo sin reconstruir el contexto.

## Cuándo termina el MVP

Cuando un usuario pueda completar el flujo integral:

**Crear gato → personalizarlo → generar seis stickers → descargar el paquete → registrarse → publicar una creación → encontrarla desde otro usuario → copiarla y personalizarla.**

Además, para la entrega académica deben cumplirse estas condiciones:

- Al menos **tres funcionalidades completas y demostrables** con persistencia y errores visibles.
- **README** con nombre, problema, instalación/ejecución, uso de IA y nombres de todos los integrantes.
- **Repositorio público** con `requirements.txt` o `pyproject.toml`, `.gitignore` correcto y mínimo 5 commits por integrante.
- **Swagger/OpenAPI** disponible para la API.
- **Sustentación de 10 minutos** ensayada, con defensa individual de cualquier módulo.
- **Guía viva** de la plataforma actualizada por incrementos.

La generación por IA debe contar con un flujo verificable independiente. Si el servicio externo no está disponible, el editor manual y la composición de stickers deben continuar funcionando. La IA es un diferenciador del producto; el PDF del curso permite usarla, pero no la exige.

## Roles del equipo

| Rol | Responsabilidad | Entregable principal |
| --- | --- | --- |
| Integrante A — Frontend y UX | Flet, navegación, editor visual, estados de generación, hub, comunicación con la API | Experiencia completa desde la creación del gato hasta la descarga |
| Integrante B — Backend y datos | Django REST Framework, MySQL, autenticación, modelos, permisos, API, Swagger, persistencia | API documentada y funcional, con pruebas de permisos y límites |
| Integrante C — Motor gráfico, IA y programación avanzada | Composición con Pillow, exportación, adaptador de IA, procesamiento de tareas, pruebas de rendimiento | Generador verificable de seis PNG y evidencias académicas reproducibles |
| Diseñadora gráfica | Guía visual, personajes base, catálogo de opciones, poses, accesorios, iconografía | Biblioteca gráfica organizada, documentada y lista para composición |

La revisión de código, las pruebas, la documentación y los ensayos de la defensa son responsabilidades compartidas. Debe existir un responsable de integración que verifique el flujo completo, no solo componentes aislados. Todos los integrantes, incluida la diseñadora, deben tener commits propios y poder explicar el funcionamiento general.

## Documentación del repositorio

| Documento | Contenido |
| --- | --- |
| [01_MASTER_PLAN.md](01_MASTER_PLAN.md) | Plan rector, cronograma de 4 semanas, hitos y dependencias críticas |
| [02_REQUIREMENTS.md](02_REQUIREMENTS.md) | Alcance P0/P1, requisitos académicos, funcionalidades, reglas de acceso, criterios de aceptación |
| [03_ARCHITECTURE.md](03_ARCHITECTURE.md) | Capas, tecnologías, estructura del repositorio, Swagger y calidad técnica |
| [04_DATA_MODEL.md](04_DATA_MODEL.md) | Entidades, relaciones, restricciones, migraciones |
| [05_API_CONTRACTS.md](05_API_CONTRACTS.md) | Endpoints, OpenAPI/Swagger, comportamiento de trabajos, errores |
| [06_DESIGN_SYSTEM.md](06_DESIGN_SYSTEM.md) | Catálogo de recursos, orden de capas, contrato con diseño |
| [07_AI_INTEGRATION.md](07_AI_INTEGRATION.md) | Alternativas de IA, flujo, seguridad, contingencia y uso de IA en el desarrollo |
| [08_CONCURRENCY_AND_PARALLELISM.md](08_CONCURRENCY_AND_PARALLELISM.md) | Casos de uso académicos, prioridad y estrategia de evidencia |
| [09_TEST_PLAN.md](09_TEST_PLAN.md) | Pruebas unitarias, integración, aceptación, seguridad, repositorio y rendimiento |
| [10_DEVELOPMENT_CHECKLIST.md](10_DEVELOPMENT_CHECKLIST.md) | Tablero de seguimiento con tareas P01–P40 |
| [11_DEMO_SCRIPT.md](11_DEMO_SCRIPT.md) | Guion de la sustentación de 10 minutos |
| [12_GUIA_PLATAFORMA.md](12_GUIA_PLATAFORMA.md) | Guía viva de funcionamiento para la preparación de la presentación |
| [13_CUMPLIMIENTO_ACADEMICO.md](13_CUMPLIMIENTO_ACADEMICO.md) | Rúbrica, entregables, commits, README y checklist de entrega |
| [decisions/](decisions/) | Registros ADR de decisiones arquitectónicas y académicas |
| [reports/](reports/) | Evidencias de rúbrica, benchmarks, pruebas de IA, instalación y auditoría |

## Cómo continuar

- Reglas y procedimiento para agentes: [`AGENTS.md`](../AGENTS.md).
- Instalación y ejecución: [README.md](../README.md) (los comandos se validan en la tarea P29).
- Antes de preparar la exposición, leer [`12_GUIA_PLATAFORMA.md`](12_GUIA_PLATAFORMA.md) y [`11_DEMO_SCRIPT.md`](11_DEMO_SCRIPT.md).
- Antes de proponer un cambio que altere el diseño, consultar [`docs/decisions/`](decisions/).

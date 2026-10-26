# 00 · Visión general del proyecto — Kitchi Studio

Documento de producto · MVP académico · Versión 1.0 · 26 de octubre de 2026

> Este es el punto de entrada obligatorio para cualquier integrante o agente de programación. Léelo antes que cualquier otro documento.

## Qué es Kitchi Studio

Nombre de trabajo, sujeto a validación de marca.

Aplicación web móvil para crear gatos chibi personalizados mediante composición de ilustraciones 2D por capas, generar paquetes de seis stickers descargables y compartibles, explorar o reutilizar personajes publicados por otros usuarios y transformar fotografías de referencia en representaciones felinas estilizadas con asistencia de IA.

**Regla central del proyecto:** construir un producto pequeño pero funcional, cuya arquitectura permita demostrar claramente los conceptos académicos, en lugar de intentar reproducir una aplicación comercial completa.

## Datos generales

| Aspecto | Valor |
| --- | --- |
| Duración | 5 semanas |
| Equipo | 3 desarrolladores + 1 diseñadora gráfica junior |
| Modalidad | Desarrollo local |
| Presupuesto | Cero |
| Entrega | Demostración visual y técnica |
| Paquete MVP | 6 stickers |
| Cliente | Web móvil |
| Arte | 2D por capas |

## Objetivo general

Desarrollar un prototipo web móvil funcional que permita crear personajes felinos de estilo chibi mediante personalización gráfica manual o transformación asistida por IA, generar paquetes de seis stickers con expresiones y poses predefinidas, descargarlos y compartirlos, y explorar o reutilizar personajes publicados por otros usuarios.

## Objetivos específicos

1. Implementar un editor de personajes mediante composición de ilustraciones 2D por capas.
2. Desarrollar un flujo de transformación de fotografías en representaciones felinas estilizadas, sujeto a la viabilidad del modelo de IA elegido.
3. Generar seis imágenes PNG con fondo transparente a partir de una configuración persistente del personaje.
4. Implementar acceso como invitado, registro, inicio de sesión y límites del plan gratuito.
5. Crear un hub donde los usuarios registrados publiquen, exploren y copien creaciones.
6. Demostrar concurrencia, multiprocesamiento y paralelismo mediante operaciones reales, medibles y documentadas.
7. Mantener documentación técnica y de producto suficiente para continuar el trabajo sin reconstruir el contexto.

## Cuándo termina el MVP

Cuando un usuario pueda completar el flujo integral:

**Crear gato → personalizarlo → generar seis stickers → descargar el paquete → registrarse → publicar una creación → encontrarla desde otro usuario → copiarla y personalizarla.**

La generación por IA debe contar con un flujo verificable independiente. Si el servicio externo no está disponible, el editor manual y la composición de stickers deben continuar funcionando.

## Roles del equipo

| Rol | Responsabilidad | Entregable principal |
| --- | --- | --- |
| Integrante A — Frontend y UX | Flet, navegación, editor visual, estados de generación, hub, comunicación con la API | Experiencia completa desde la creación del gato hasta la descarga |
| Integrante B — Backend y datos | Django REST Framework, MySQL, autenticación, modelos, permisos, API, persistencia | API documentada y funcional, con pruebas de permisos y límites |
| Integrante C — Motor gráfico, IA y programación avanzada | Composición con Pillow, exportación, adaptador de IA, procesamiento de tareas, pruebas de rendimiento | Generador verificable de seis PNG y evidencias académicas reproducibles |
| Diseñadora gráfica | Guía visual, personajes base, catálogo de opciones, poses, accesorios, iconografía | Biblioteca gráfica organizada, documentada y lista para composición |

La revisión de código, las pruebas y la documentación son responsabilidades compartidas. Debe existir un responsable de integración que verifique el flujo completo, no solo componentes aislados.

## Documentación del repositorio

| Documento | Contenido |
| --- | --- |
| [01_MASTER_PLAN.md](01_MASTER_PLAN.md) | Plan rector, cronograma, hitos y dependencias críticas |
| [02_REQUIREMENTS.md](02_REQUIREMENTS.md) | Alcance P0/P1, funcionalidades, reglas de acceso, criterios de aceptación |
| [03_ARCHITECTURE.md](03_ARCHITECTURE.md) | Capas, tecnologías, estructura del repositorio |
| [04_DATA_MODEL.md](04_DATA_MODEL.md) | Entidades, relaciones, restricciones, migraciones |
| [05_API_CONTRACTS.md](05_API_CONTRACTS.md) | Endpoints, comportamiento de trabajos, errores |
| [06_DESIGN_SYSTEM.md](06_DESIGN_SYSTEM.md) | Catálogo de recursos, orden de capas, contrato con diseño |
| [07_AI_INTEGRATION.md](07_AI_INTEGRATION.md) | Alternativas de IA, flujo, seguridad, contingencia |
| [08_CONCURRENCY_AND_PARALLELISM.md](08_CONCURRENCY_AND_PARALLELISM.md) | Casos de uso académicos y estrategia de evidencia |
| [09_TEST_PLAN.md](09_TEST_PLAN.md) | Pruebas unitarias, integración, aceptación, seguridad, rendimiento |
| [10_DEVELOPMENT_CHECKLIST.md](10_DEVELOPMENT_CHECKLIST.md) | Tablero de seguimiento con tareas P01–P30 |
| [11_DEMO_SCRIPT.md](11_DEMO_SCRIPT.md) | Guion de la demostración académica |
| [decisions/](decisions/) | Registros ADR de decisiones arquitectónicas |
| [reports/](reports/) | Evidencias de benchmarks, pruebas de IA e instalación |

## Cómo continuar

- Reglas y procedimiento para agentes: [`AGENTS.md`](../AGENTS.md).
- Instalación y ejecución: [README.md](../README.md) (pendiente de completar con comandos verificados).
- Antes de proponer un cambio que altere el diseño, consultar [`docs/decisions/`](decisions/).

# 01 · Plan maestro — Kitchi Studio

Plan rector del proyecto · Versión 1.0 · 26 de octubre de 2026

> Resumen operativo del plan maestro. El documento original completo se conserva en [`project.md`](../project.md). Este archivo define el cronograma, los hitos, las dependencias y el protocolo de decisiones.

## Estrategia general

- Enfoque 2D por capas: el motor combina recursos compatibles; no se producen las 3⁶ = 729 combinaciones como imágenes independientes, sino un catálogo inicial de 18 opciones conceptuales (3 por cada uno de los 6 campos).
- Comenzar por el motor gráfico y los contratos de API.
- Validar la IA en la primera semana, antes de comprometerse con un modelo concreto.
- Reservar la última semana para estabilización y demostración, no para funcionalidades nuevas.
- Resultado funcional desde la primera semana, para descubrir los riesgos técnicos temprano.

## Cronograma de cinco semanas

### Semana 1 — Validación y cimientos (fundacional)

Objetivo: eliminar las incertidumbres que podrían bloquear el MVP.

- Confirmar la rúbrica con el profesor.
- Crear repositorio, estructura documental y reglas de agentes.
- Validar Flet web móvil, Django y conexión a MySQL.
- Componer un gato con varias capas reales.
- Comparar opciones de IA con una prueba mínima.
- Aprobar contratos iniciales de API y catálogo gráfico.
- Preparar un ejemplo de benchmark de procesamiento.

**Hito:** un gato visible desde recursos 2D y una decisión fundamentada sobre IA y arquitectura.

### Semana 2 — Editor y persistencia (funcional)

- Implementar navegación principal.
- Implementar selectores de las seis categorías.
- Crear modelos y migraciones.
- Implementar registro e inicio de sesión.
- Guardar y recuperar configuraciones de gatos.
- Aplicar el límite de tres gatos.

**Hito:** un usuario puede personalizar un gato, guardarlo y recuperarlo.

### Semana 3 — Stickers e IA (generación)

- Implementar las seis poses.
- Componer imágenes mediante Pillow.
- Exportar PNG transparentes.
- Implementar el registro y seguimiento de trabajos.
- Integrar la IA elegida.
- Implementar errores, límites y reintentos.

**Hito:** un usuario puede generar y descargar un paquete completo.

### Semana 4 — Hub y requisitos académicos (integración)

- Implementar publicación y exploración del hub.
- Implementar copia de creaciones públicas.
- Demostrar concurrencia con operaciones reales.
- Implementar multiprocesamiento para trabajos gráficos.
- Ejecutar benchmarks secuenciales y paralelos.
- Verificar permisos, límites y privacidad.

**Hito:** el flujo comunitario funciona y existen evidencias técnicas de los tres conceptos.

### Semana 5 — Pruebas y entrega (estabilización)

- Ejecutar pruebas unitarias, de integración y de aceptación.
- Corregir errores críticos.
- Verificar que el proyecto se instala desde un clon limpio.
- Preparar datos de demostración.
- Documentar resultados de rendimiento.
- Ensayar la exposición académica.
- Congelar versiones y etiquetar la entrega.

**Hito:** prototipo demostrable, reproducible y documentado.

## Dependencias críticas

1. El editor no puede finalizarse sin una convención de recursos gráficos.
2. El backend no puede integrarse con el frontend sin contratos de API.
3. El generador de stickers debe funcionar antes de incorporar paralelismo.
4. La demostración académica debe prepararse antes de la última semana.

La prueba de IA se realizará en la primera semana. No se dejará para después de terminar el editor.

## Regla para recuperar retrasos

- Si al final de la **semana 2** el editor y la persistencia todavía no funcionan → se congelan las funcionalidades P1.
- Si al final de la **semana 3** la IA no está integrada → se documenta el motivo y se aplica el plan de contingencia ([07_AI_INTEGRATION.md](07_AI_INTEGRATION.md)), sin comprometer la generación manual de stickers.
- La última semana no se usa para funcionalidades nuevas.

## Condiciones técnicas que deben verificarse en la semana 1

Antes de desarrollar todas las pantallas, validar ([sesión 3.3 del plan original](../project.md)):

- Que la versión elegida de Flet permita servir el prototipo web móvil como se espera.
- Que el cliente Flet pueda comunicarse correctamente con la API de Django.
- Que la autenticación elegida funcione con el cliente y con las peticiones de descarga.
- Que Pillow pueda componer los recursos gráficos en el formato requerido.
- Que el método de IA elegido permita ejecutar una prueba real sin pago.
- Que la herramienta de desarrollo y las versiones de Python sean compatibles.

Las versiones exactas se fijan en los archivos de dependencias una vez comprobadas. No usar versiones flotantes ni actualizar dependencias a mitad del proyecto sin razón concreta.

## Decisiones pendientes y protocolo de aprobación

| Prioridad | Decisión pendiente | Responsable sugerido | Fecha límite |
| --- | --- | --- | --- |
| Crítica | Rúbrica exacta de concurrencia, multiprocesamiento, paralelismo e IA | Todo el equipo | Día 1 |
| Crítica | Prueba real de IA sin coste | Integrante C | Día 3 |
| Crítica | Compatibilidad del prototipo web con Flet | Integrante A | Día 2 |
| Crítica | Primer gato completo y contrato de capas | Diseñadora + C | Día 3 |
| Alta | Contratos iniciales de API | A + B | Día 3 |
| Alta | Esquema inicial de datos y autenticación | Integrante B | Día 4 |
| Alta | Formato definitivo de recursos y poses | Diseñadora + C | Día 4 |
| Alta | Mecanismo de autenticación entre Flet y Django | A + B | Día 4 |
| Media | Persistencia de invitados y recuperación de sesiones | A + B | Semana 2 |
| Media | Comportamiento visual del plan premium simulado | A + diseñadora | Semana 2 |

Estas fechas son objetivos internos, no garantías. Si una prueba crítica falla, se registra el problema y se toma una decisión explícita en [`decisions/`](decisions/) en vez de continuar suponiendo que se resolverá más adelante.

## Preguntas que deben hacerle al profesor

1. ¿Se exige implementar `threading`, `multiprocessing`, `asyncio` o alguna biblioteca concreta?
2. ¿Deben demostrarse los tres conceptos por separado o basta con una solución integrada?
3. ¿La IA debe utilizar un modelo de aprendizaje automático real? ¿Se permite un modelo preentrenado o un servicio externo?
4. ¿Se exige entrenamiento del modelo o es suficiente la inferencia?
5. ¿Debe existir una medición de rendimiento que compare ejecución secuencial y paralela?
6. ¿Se requiere una cantidad mínima de procesos, hilos o tareas concurrentes?
7. ¿Se calificará el uso de la base de datos, las pruebas automatizadas y la documentación?
8. ¿Qué peso tiene la aplicación funcional frente a la exposición y las evidencias técnicas?

Las respuestas pueden cambiar el orden de trabajo y la selección del modelo de IA, pero no la visión central del producto. Registrar la rúbrica obtenida en [`reports/`](reports/).

## Primeras 72 horas

### Día 1 — Organización

- Crear el repositorio.
- Añadir `AGENTS.md` y la documentación inicial. ✅ (esta estructura)
- Consultar al profesor.
- Asignar responsables y establecer el mecanismo de revisión de cambios.

### Día 2 — Pruebas técnicas

- Crear una aplicación mínima con Flet.
- Crear una API mínima con Django REST Framework.
- Conectar Django a MySQL.
- Componer un gato con dos o tres capas.
- Registrar tiempos de composición.

### Día 3 — Validación de riesgos

- Probar el servicio o modelo de IA.
- Evaluar el resultado gráfico.
- Verificar compatibilidad del entorno.
- Aprobar la primera guía de recursos.
- Registrar las decisiones técnicas definitivas en [`decisions/`](decisions/).

**Al finalizar:** repositorio que arranca, un primer recurso gráfico componible, una API conectada a la base de datos y una decisión sustentada sobre la viabilidad de IA.

## Definición final del éxito

El proyecto se mide por la coherencia del sistema completo, no por la cantidad de pantallas o tecnologías. Un buen MVP cumple cinco condiciones:

1. **Producto:** el usuario puede crear un gato y obtener un paquete de stickers real.
2. **Diseño:** las combinaciones son personalizables pero pertenecen a un lenguaje visual reconocible.
3. **Arquitectura:** interfaz, API, base de datos, almacenamiento y motor de generación tienen responsabilidades claras.
4. **Rigor académico:** la IA, la concurrencia, el multiprocesamiento y el paralelismo se explican y demuestran con evidencias.
5. **Reproducibilidad:** un integrante nuevo o un evaluador puede comprender el repositorio, instalar el proyecto y repetir las pruebas.

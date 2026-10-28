# 02 · Requisitos y alcance — Kitchi Studio

Requisitos funcionales, alcance, requisitos académicos y criterios de aceptación · Versión 1.1 · 28 de octubre de 2026

> La restricción más importante no es solo el tiempo de programación: es la combinación de diseño gráfico, editor interactivo, procesamiento de imágenes, integración de IA y backend, con una fecha límite de **cuatro semanas**. El alcance se divide en tres niveles y no debe expandirse sin registrar la decisión. Los requisitos académicos del PDF del profesor son obligatorios y están detallados en [`13_CUMPLIMIENTO_ACADEMICO.md`](13_CUMPLIMIENTO_ACADEMICO.md).

## Alcance

### P0 — Núcleo obligatorio para la entrega

- Editor de gatos 2D por capas.
- Tres opciones por cada campo de personalización.
- Seis stickers por paquete.
- Exportación PNG transparente.
- Invitado y cuenta registrada.
- Límite de tres gatos para usuarios gratuitos.
- Publicar, explorar y copiar personajes.
- **Al menos tres funcionalidades completas y demostrables** (ver sección siguiente).
- **Interfaz real** (Flet Web), no una aplicación de solo consola.
- **Persistencia** de cuentas, gatos, publicaciones y paquetes.
- **Manejo de errores visible** en la interfaz y en la API.
- **Swagger/OpenAPI** disponible para la API.
- **README completo** con nombre, problema, instalación/ejecución, uso de IA y nombres de los integrantes.
- **Repositorio público** con `requirements.txt` o `pyproject.toml`, `.gitignore` correcto y mínimo 5 commits descriptivos por integrante.
- **Guía viva de la plataforma** actualizada por incrementos.
- **Sustentación de 10 minutos** ensayada, con defensa individual.

### P0 — Diferenciadores (deseables, no bloqueantes)

- IA integrada o, como mínimo, una integración real demostrable con un flujo de contingencia documentado.
- Evidencias de concurrencia, multiprocesamiento y paralelismo, como diferenciador de calidad técnica.

> Si un diferenciador falla, se documenta la contingencia y se prioriza el núcleo obligatorio. No se presenta una función simulada como si fuera real.

### P1 — Solo después de completar P0

- Favoritos.
- Perfil público más elaborado.
- Búsqueda y filtros avanzados del hub.
- Guardado de paquetes completos en la cuenta.
- Indicador visual de tareas de generación en cola.
- Simulación de catálogo premium.

### Fuera del MVP

- Pagos o suscripciones reales.
- Aplicación nativa publicada en tiendas.
- Integración directa con WhatsApp como paquete instalable.
- Modelos 3D y animaciones 3D.
- Entrenamiento de un modelo propio.
- Entrenamiento personalizado por usuario.
- Infraestructura de producción distribuida.
- Mensajería privada, comentarios y red social completa.

## Tres funcionalidades completas mínimas

La rúbrica exige al menos tres funcionalidades completas y demostrables. Para este proyecto se consideran:

| # | Funcionalidad | Inicio | Fin | Evidencia |
| --- | --- | --- | --- | --- |
| 1 | Editor de personajes | Crear un gato | Guardar y recuperar la configuración personalizada | AC-01, AC-02 |
| 2 | Generación y descarga de stickers | Solicitar el paquete | Descargar seis PNG transparentes | AC-03, AC-04 |
| 3 | Cuenta y comunidad | Registrarse / iniciar sesión | Publicar, explorar y copiar sin alterar el original | AC-05…AC-07 |

La **IA** es un cuarto flujo deseable y un diferenciador, no una de las tres funcionalidades mínimas. Si falla, se documenta la contingencia (AC-08) y las tres anteriores siguen siendo demostrables.

## Requisitos académicos del curso

Estos requisitos provienen del PDF del profesor y se verifican con la auditoría de [`reports/academic-audit.md`](reports/academic-audit.md):

| ID | Requisito | Criterio de verificación |
| --- | --- | --- |
| AR-01 | Aplicación real con interfaz, no solo consola | Flet Web operativo y demostrable |
| AR-02 | Backend con endpoints y persistencia | API DRF + MySQL |
| AR-03 | Al menos 3 funcionalidades completas | Tabla anterior y escenario de aceptación |
| AR-04 | Datos persistentes | Reinicio y recuperación de datos |
| AR-05 | Errores visibles para el usuario | Pruebas de error en UI y API |
| AR-06 | Swagger/OpenAPI | `/api/docs/` y `/api/schema/` |
| AR-07 | README completo | Checklist de [`README.md`](../README.md) |
| AR-08 | Sección “Uso de IA” | README y [`07_AI_INTEGRATION.md`](07_AI_INTEGRATION.md) |
| AR-09 | Nombres de todos los integrantes | README |
| AR-10 | Repositorio público y organizado | Enlace y estructura |
| AR-11 | Mínimo 5 commits por integrante | `git shortlog -sne --all` |
| AR-12 | Dependencias declaradas | `requirements.txt` o `pyproject.toml` |
| AR-13 | `.gitignore` correcto, sin secretos | Auditoría de Git |
| AR-14 | Sustentación de 10 minutos | Guion y ensayo |
| AR-15 | Defensa individual de cualquier módulo | Guía viva y preguntas de ensayo |

## Editor de personajes

Cada campo tendrá tres alternativas seleccionables. Las alternativas son recursos gráficos predefinidos, no piezas dibujadas en tiempo real.

| Campo | Tres alternativas conceptuales |
| --- | --- |
| Patrón y colores del pelaje | Atigrado naranja, bicolor, manchas oscuras |
| Ojos y color | Redondos verdes, grandes azules, almendrados ámbar |
| Cabello y color | Flequillo corto, mechones laterales, cabello ondulado |
| Parte superior | Camiseta, sudadera, camisa |
| Parte inferior | Pantalón corto, falda, pantalón largo |
| Accesorios | Gafas, lazo, gorro |

Reglas:

- Las combinaciones deben seguir reglas de compatibilidad: una prenda puede ocultar una parte del cuerpo y el accesorio debe renderizarse delante o detrás de la cabeza según corresponda.
- Tres opciones por campo significan un catálogo inicial de **18 opciones conceptuales**, no 729 ilustraciones independientes. El motor combina recursos compatibles; las 3⁶ = 729 combinaciones teóricas no requieren producción anticipada.
- El catálogo debe ser validado por el backend; el cliente no puede enviar nombres de archivos arbitrarios.

## Poses del generador de stickers

Seis poses estáticas reutilizables:

1. Saludo
2. Alegría
3. Enfado
4. Tristeza
5. Sorpresa
6. Sueño o descanso

La diseñadora produce las piezas y las poses siguiendo una guía de proporciones, anclajes y orden de capas ([06_DESIGN_SYSTEM.md](06_DESIGN_SYSTEM.md)). La consistencia no puede depender únicamente de instrucciones de texto a una IA.

## Pantallas mínimas y navegación

La aplicación debe sentirse como un juego de vestir personajes, no como un formulario administrativo. Inspiración en la accesibilidad de los juegos de personalización y la expresividad de los stickers, sin copiar recursos gráficos ni interfaces exactas.

Flujo de navegación: Inicio → Explorar hub / Crear gato / Mis gatos / Iniciar sesión · Registrarse → Elegir método (manual o fotografía con IA) → Personalización → Revisar resultado IA → Previsualizar personaje → Generar 6 stickers → Vista previa del paquete → Descargar PNG / Guardar paquete · Publicar creación → Ver personaje publicado → Copiar personaje.

| Pantalla | Elementos esenciales | Criterio de finalización |
| --- | --- | --- |
| Inicio | Acceso al editor y al hub | Permite iniciar los flujos principales |
| Editor | Vista del gato, seis selectores y controles de navegación | Las seis categorías actualizan la apariencia |
| Importación de fotografía | Selección de archivo, vista previa y envío a IA | Valida formato, tamaño y errores |
| Revisión de IA | Imagen generada y opciones para continuar o reintentar | El resultado puede pasar al flujo de creación |
| Generador | Seis poses, indicador de progreso y estado | Produce seis imágenes válidas |
| Paquete | Vista previa, descarga y opción de guardar | Se descargan los archivos esperados |
| Registro e inicio de sesión | Formularios y validación | Se crea una sesión autenticada |
| Hub | Galería de creaciones públicas | Permite abrir una creación y copiar su configuración |
| Publicación | Nombre, descripción y visibilidad | Una creación se publica y queda disponible en el hub |
| Mis gatos | Lista de personajes propios | Permite abrir, editar y eliminar creaciones propias |

## Reglas de acceso

### Invitado

- Puede crear hasta tres gatos en el dispositivo o sesión local.
- Puede personalizar y generar paquetes.
- Puede descargar los PNG.
- Puede copiar personajes públicos.
- No puede publicar en el hub.
- Sus datos locales pueden perderse al borrar los datos del navegador. **Esta limitación debe explicarse al usuario.**

### Usuario registrado

- Puede crear y guardar hasta tres gatos en el plan gratuito.
- Puede publicar y explorar creaciones públicas.
- Puede copiar una creación a su propio editor sin modificar el original.
- Puede gestionar sus publicaciones y sus gatos.
- No puede editar ni eliminar las creaciones de otro usuario.

### Premium simulado

- El MVP no debe tener cobros reales.
- El catálogo premium se representa con opciones bloqueadas, un indicador visual y una simulación controlada para la demostración.

**Aplicación de límites:** la restricción de tres gatos se comprueba en el backend para usuarios registrados; la interfaz por sí sola no constituye un mecanismo de control. En modo invitado se puede usar almacenamiento local, pero no debe presentarse como protección contra la manipulación.

## Criterios de aceptación generales

El MVP se considerará entregable cuando satisfaga **todos** los criterios obligatorios. Los criterios AC-01…AC-14 son de producto; AC-15…AC-22 son académicos y provienen del PDF.

| ID | Criterio | Evidencia |
| --- | --- | --- |
| AC-01 | El editor permite modificar las seis categorías | Prueba funcional y captura |
| AC-02 | Las opciones se componen sin perder la coherencia visual | Paquete de personajes de prueba |
| AC-03 | Se genera un paquete con seis stickers PNG | Archivos de salida verificables |
| AC-04 | Los PNG conservan transparencia | Prueba de canal alfa |
| AC-05 | Un usuario gratuito no supera tres gatos guardados | Prueba de límite |
| AC-06 | Registro e inicio de sesión funcionan | Pruebas de autenticación |
| AC-07 | Las publicaciones pueden explorarse y copiarse | Prueba entre dos cuentas |
| AC-08 | La IA ejecuta una inferencia real en el flujo acordado | Entrada, salida y registro del trabajo |
| AC-09 | Se demuestra concurrencia con operaciones reales | Logs y pruebas de tareas |
| AC-10 | Se demuestra multiprocesamiento | Identificación de procesos y resultados |
| AC-11 | Se mide el procesamiento secuencial y paralelo | Informe reproducible |
| AC-12 | El repositorio contiene documentación actualizada | Revisión de archivos |
| AC-13 | El proyecto arranca desde un clon limpio | Registro de instalación y ejecución |
| AC-14 | No se exponen secretos ni imágenes privadas por defecto | Revisión de configuración y permisos |
| AC-15 | El README contiene nombre, problema, instalación, uso de IA e integrantes | Checklist de README |
| AC-16 | Existe `requirements.txt` o `pyproject.toml` con versiones fijadas | Revisión de archivos |
| AC-17 | El repositorio es público y tiene mínimo 5 commits por integrante | `git shortlog` y enlace |
| AC-18 | Swagger/OpenAPI está disponible y actualizado | `/api/docs/` y `/api/schema/` |
| AC-19 | La aplicación tiene interfaz real, 3 funcionalidades completas, persistencia y errores visibles | Escenario de aceptación |
| AC-20 | Cada integrante puede explicar cualquier módulo y navegar el código | Ensayo individual |
| AC-21 | La sustentación se ejecuta en 10 minutos | Ensayo cronometrado |
| AC-22 | La guía viva de la plataforma está actualizada | Revisión de `12_GUIA_PLATAFORMA.md` |

> AC-09, AC-10 y AC-11 son diferenciadores de calidad técnica: el PDF del curso no los exige explícitamente. No deben comprometer AC-01…AC-08 ni AC-15…AC-22.

## Escenario de aceptación principal

Recorrido integral que el evaluador debe poder repetir sin editar la base de datos manualmente (detalle en [09_TEST_PLAN.md](09_TEST_PLAN.md)):

1. Clonar el repositorio y seguir el README sin pasos no documentados.
2. Abrir Swagger y comprobar que la API está documentada.
3. Entrar como invitado y crear un gato.
4. Modificar las seis categorías y comprobar los cambios visuales.
5. Generar el paquete de seis stickers.
6. Descargar y abrir los PNG para comprobar que tienen fondo transparente.
7. Crear una cuenta e iniciar sesión.
8. Publicar el personaje y encontrarlo desde otra sesión.
9. Copiar el personaje y verificar que editar la copia no altera el original.
10. Ejecutar la demostración de IA y mostrar el manejo de errores.
11. Ejecutar las pruebas de concurrencia y mostrar los resultados del benchmark.
12. Mostrar que los datos persisten tras reiniciar la aplicación.
13. Recorrer el repositorio y explicar un módulo elegido por el profesor.

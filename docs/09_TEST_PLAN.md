# 09 · Plan de pruebas y control de calidad — Kitchi Studio

Pruebas unitarias, de integración, aceptación, seguridad y rendimiento · Versión 1.0

> Las pruebas validan tanto el funcionamiento del producto como los requisitos de programación avanzada. El criterio de aceptación no es que las pantallas se vean bien en una captura: se debe poder ejecutar el recorrido completo con datos reales de prueba.

## Pruebas unitarias

Se prueban de forma aislada:

- Validación de configuraciones de gatos.
- Reglas del catálogo.
- Límite de tres gatos.
- Composición de capas.
- Exportación PNG.
- Transiciones de estados de trabajos.
- Permisos de publicaciones.
- Cálculo de rutas y nombres de archivos.
- Validación de archivos de entrada para IA.

Ubicación: `backend/tests/`, `frontend/tests/` y los módulos de evidencia de concurrencia ([08_CONCURRENCY_AND_PARALLELISM.md](08_CONCURRENCY_AND_PARALLELISM.md)).

## Pruebas de integración

| Prueba | Resultado esperado |
| --- | --- |
| Flet consulta el catálogo | Obtiene las opciones activas de la API |
| Usuario registra un gato | El registro persiste en MySQL |
| Se solicita un paquete | Se crea un trabajo y se devuelve un identificador |
| Termina el trabajo | El estado cambia a `completed` y existen seis PNG |
| Falla una pose | El fallo se registra y no se declara éxito completo sin validar el paquete |
| Usuario publica un gato | La publicación aparece en el hub |
| Otro usuario copia el gato | Se crea una copia independiente |
| Invitado intenta publicar | La API rechaza la operación |
| Usuario intenta editar un gato ajeno | La API rechaza la operación |
| Usuario supera el límite gratuito | La API impide la creación adicional |

## Pruebas de aceptación

### Escenario de aceptación principal

El evaluador debe poder repetir este recorrido **sin editar la base de datos manualmente**:

1. Entrar como invitado y crear un gato.
2. Modificar las seis categorías y comprobar los cambios visuales.
3. Generar el paquete de seis stickers.
4. Descargar y abrir los PNG para comprobar que tienen fondo transparente.
5. Crear una cuenta e iniciar sesión.
6. Publicar el personaje y encontrarlo desde otra sesión.
7. Copiar el personaje y verificar que editar la copia no altera el original.
8. Ejecutar la demostración de IA y mostrar el manejo de errores.
9. Ejecutar las pruebas de concurrencia y mostrar los resultados del benchmark.

Cada paso se traza con un criterio de aceptación de [02_REQUIREMENTS.md](02_REQUIREMENTS.md) (AC-01 … AC-14) y su evidencia se archiva en [`reports/`](reports/).

## Pruebas de seguridad

- Contraseñas gestionadas por Django.
- Protección de endpoints privados.
- Verificación de propiedad en operaciones de modificación y eliminación.
- Validación de archivos subidos.
- Restricción de tipos de archivo.
- Configuración segura de CORS.
- Secretos fuera del repositorio.
- Eliminación de fotografías temporales.
- Control de errores para no exponer trazas internas.
- Prevención de acceso a archivos mediante rutas manipuladas.

## Pruebas de rendimiento

Para la demostración se recomienda medir:

- Tiempo de composición de un sticker.
- Tiempo de generación de seis stickers.
- Tiempo secuencial frente a multiproceso.
- Número de procesos trabajadores.
- Número de tareas completadas y fallidas.
- Tiempo de respuesta de la API.
- Latencia de IA, por separado de la composición gráfica.

**Metodología:** se registran el equipo utilizado, la versión de Python, el tamaño de las imágenes, el número de repeticiones y la metodología. Las mediciones deben ser reproducibles y **no se presentan como garantías de rendimiento en producción**. Herramienta: `scripts/benchmark_generation.py`; resultados en [`reports/benchmark.md`](reports/).

## Protocolo de instalación reproducible (AC-13)

La entrega debe ser reproducible: otro integrante o evaluador debe poder clonar el repositorio y ejecutar el proyecto siguiendo instrucciones documentadas, sin depender de configuraciones personales no registradas.

La documentación de instalación ([README.md](../README.md), sección pendiente de comandos verificados) incluirá:

- [ ] Versiones de Python y dependencias.
- [ ] Requisitos previos de MySQL.
- [ ] Creación y configuración de la base de datos.
- [ ] Variables de entorno requeridas (ver [`.env.example`](../.env.example)).
- [ ] Comandos de migración y carga de datos de demostración (`scripts/seed_demo_data.py`).
- [ ] Comandos para iniciar backend y frontend.
- [ ] Comandos para ejecutar las pruebas.
- [ ] Comando para ejecutar el benchmark.
- [ ] Solución de errores comunes.

Los comandos se mantienen en el `README.md`, separando la configuración del backend y del frontend cuando sea necesario. Los archivos de dependencias deben estar fijados a versiones verificadas.

## Ejecución en el cronograma

- Semana 4 (P23): pruebas de permisos y límites.
- Semana 5 (P24–P25): pruebas de aceptación y corrección de errores críticos.
- Semana 5 (P29): verificar instalación desde un clon limpio.

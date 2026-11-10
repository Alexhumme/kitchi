# 09 · Plan de pruebas y control de calidad — Kitchi Studio

Pruebas unitarias, integración, aceptación, seguridad, repositorio y rendimiento · Versión 1.1 · 28 de octubre de 2026

> Las pruebas validan tanto el funcionamiento del producto como los requisitos académicos. El criterio de aceptación no es que las pantallas se vean bien en una captura: se debe poder ejecutar el recorrido completo con datos reales de prueba, desde un clon limpio y sin editar la base de datos a mano.

## Pruebas unitarias

Se prueban de forma aislada:

- Validación de configuraciones de gatos.
- Reglas del catálogo.
- Límite de tres gatos.
- Composición de capas.
- Exportación PNG.
- Verificación de dimensiones y canal alfa.
- Transiciones de estados de trabajos.
- Permisos de publicaciones.
- Cálculo de rutas y nombres de archivos.
- Validación de archivos de entrada para IA.
- Serializers y permisos de la API.
- Manejo de errores y mensajes al usuario.

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
| Se reinicia la aplicación | Los datos persisten y se recuperan |
| Se abre `/api/docs/` | Swagger muestra los endpoints y permite probarlos |
| Se provoca un error de validación | La UI muestra un mensaje comprensible y la API no expone trazas internas |

Estado al 9 de noviembre de 2026: las filas de catálogo, registro y persistencia de gatos
están cubiertas por `frontend/tests/` (34 pruebas) y por el cliente HTTP; las de paquetes,
publicaciones, copia e IA siguen pendientes porque sus endpoints no existen. La prueba
manual en navegador aún no se registra en `docs/reports/`.

## Pruebas de aceptación

### Escenario de aceptación principal

El evaluador debe poder repetir este recorrido **sin editar la base de datos manualmente**:

1. Clonar el repositorio y seguir el README sin pasos no documentados.
2. Abrir `/api/docs/` y comprobar que la API está documentada.
3. Entrar como invitado y crear un gato.
4. Modificar las seis categorías y comprobar los cambios visuales.
5. Generar el paquete de seis stickers.
6. Descargar y abrir los PNG para comprobar que tienen fondo transparente.
7. Crear una cuenta e iniciar sesión.
8. Publicar el personaje y encontrarlo desde otra sesión.
9. Copiar el personaje y verificar que editar la copia no altera el original.
10. Ejecutar la demostración de IA y mostrar el manejo de errores.
11. Ejecutar las pruebas de concurrencia y mostrar los resultados del benchmark.
12. Reiniciar la aplicación y comprobar que los datos persisten.
13. Recorrer el repositorio y explicar un módulo elegido por el profesor.

Cada paso se traza con un criterio de aceptación de [02_REQUIREMENTS.md](02_REQUIREMENTS.md) (AC-01…AC-22) y su evidencia se archiva en [`reports/`](reports/).

## Pruebas académicas y de repositorio

Estas pruebas se ejecutan antes de la entrega interna y se registran en [`reports/academic-audit.md`](reports/academic-audit.md):

| Prueba | Cómo se verifica | Evidencia |
| --- | --- | --- |
| README completo | Checklist de secciones obligatorias | `reports/readme-check.md` |
| Dependencias declaradas | `requirements.txt` o `pyproject.toml` con versiones | Revisión de archivos |
| `.gitignore` correcto | `git ls-files` sin `.env`, `__pycache__`, `.pyc`, bases locales | `reports/commits-audit.md` |
| Commits por integrante | `git shortlog -sne --all` con ≥5 por persona | `reports/commits-audit.md` |
| Sin secretos | Búsqueda de claves, tokens y contraseñas; `.env` fuera de Git | `reports/commits-audit.md` |
| Swagger | `/api/docs/` carga y documenta los endpoints | Captura y prueba |
| Tres funcionalidades | Escenario de aceptación de los pasos 3–10 | `reports/acceptance-run.md` |
| Errores visibles | Pruebas de error en UI y API | `reports/acceptance-run.md` |
| Instalación limpia | Clonar en un directorio nuevo y seguir el README | `reports/clean-install.md` |
| Guía viva actualizada | Revisión de `12_GUIA_PLATAFORMA.md` | Revisión cruzada |
| Defensa individual | Cada integrante explica un módulo ajeno | `reports/defense-rehearsal.md` |
| Demo de 10 minutos | Ensayo cronometrado | `reports/defense-rehearsal.md` |

### Comandos de auditoría

```bash
git shortlog -sne --all
git log --oneline --all
git ls-files | Select-String -Pattern "\.env$|__pycache__|\.pyc$|\.sqlite3?$"
git grep -n -I -E "API_KEY|SECRET_KEY|PASSWORD|TOKEN" -- ":!*.example" ":!docs/**"
```

> Ejecutar en PowerShell o Git Bash. No imprimir valores reales de secretos en la salida compartida.

## Pruebas de seguridad

- Contraseñas gestionadas por Django.
- Protección de endpoints privados.
- Verificación de propiedad en operaciones de modificación y eliminación.
- Validación de archivos subidos.
- Restricción de tipos de archivo.
- Configuración segura de CORS.
- Secretos fuera del repositorio y cargados con `python-dotenv`.
- Eliminación de fotografías temporales.
- Control de errores para no exponer trazas internas.
- Prevención de acceso a archivos mediante rutas manipuladas.
- Sin datos personales reales en los datos de demostración.

## Pruebas de rendimiento

Para la demostración se recomienda medir:

- Tiempo de composición de un sticker.
- Tiempo de generación de seis stickers.
- Tiempo secuencial frente a multiproceso.
- Número de procesos trabajadores.
- Número de tareas completadas y fallidas.
- Tiempo de respuesta de la API.
- Latencia de IA, por separado de la composición gráfica.

**Metodología:** se registran el equipo utilizado, la versión de Python, el tamaño de las imágenes, el número de repeticiones y la metodología. Las mediciones deben ser reproducibles y **no se presentan como garantías de rendimiento en producción**. Herramienta: `scripts/benchmark_generation.py`; resultados en [`reports/benchmark.md`](reports/benchmark.md).

## Protocolo de instalación reproducible (AC-13 / criterio 5)

La entrega debe ser reproducible: otro integrante o evaluador debe poder clonar el repositorio y ejecutar el proyecto siguiendo instrucciones documentadas, sin depender de configuraciones personales no registradas.

La documentación de instalación ([`README.md`](../README.md)) debe incluir:

- [ ] Versiones de Python y dependencias fijadas.
- [ ] Requisitos previos de MySQL.
- [ ] Creación y configuración de la base de datos.
- [ ] Variables de entorno requeridas (ver [`.env.example`](../.env.example)).
- [ ] Comandos de migración y carga de datos de demostración (`scripts/seed_demo_data.py`).
- [ ] Comandos para iniciar backend y frontend.
- [ ] Comandos para abrir Swagger.
- [ ] Comandos para ejecutar las pruebas.
- [ ] Comando para ejecutar el benchmark.
- [ ] Solución de errores comunes.
- [ ] Verificación de que no se requiere editar archivos del repositorio a mano.

Los comandos se mantienen en el `README.md`, separando la configuración del backend y del frontend cuando sea necesario. Los archivos de dependencias deben estar fijados a versiones verificadas.

## Pruebas de documentación y sustentación

- La guía viva [`12_GUIA_PLATAFORMA.md`](12_GUIA_PLATAFORMA.md) debe describir el flujo real, no el diseñado.
- Cada integrante debe poder explicar cualquier módulo y navegar el repositorio en vivo.
- El guion de [`11_DEMO_SCRIPT.md`](11_DEMO_SCRIPT.md) debe ejecutarse en 10 minutos, incluyendo preguntas.
- La demo debe distinguir claramente entre funcionalidad real, funcionalidad simulada y contingencia.
- El README debe reflejar el estado real del proyecto; no se documentan funciones inexistentes.

## Ejecución en el cronograma

- Semana 2: pruebas de modelos, permisos y autenticación.
- Semana 3 (P23): pruebas de permisos, límites, generación y errores.
- Semana 4 (P24–P25): aceptación, corrección de errores críticos y congelación.
- Semana 4 (P29): instalación desde un clon limpio.
- Semana 4 (P37/P40): ensayo de la defensa y auditoría académica final.

## Matriz de evidencia

| Evidencia | AC | AR | Archivo |
| --- | --- | --- | --- |
| Editor y seis categorías | AC-01, AC-02 | AR-03 | `reports/acceptance-run.md` |
| Seis PNG transparentes | AC-03, AC-04 | AR-03 | `reports/acceptance-run.md` |
| Límite de tres gatos | AC-05 | AR-03 | Pruebas de integración |
| Registro y login | AC-06 | AR-03 | Pruebas de autenticación |
| Hub y copia | AC-07 | AR-03 | `reports/acceptance-run.md` |
| IA real o contingencia | AC-08 | AR-03 | `reports/ai-evaluation.md` |
| Concurrencia / paralelismo | AC-09…AC-11 | Diferenciador | `reports/concurrency-logs.md`, `reports/benchmark.md` |
| Documentación | AC-12, AC-22 | AR-07, AR-15 | Docs y guía viva |
| Clon limpio | AC-13 | Criterio 5 | `reports/clean-install.md` |
| Sin secretos | AC-14 | AR-13 | `reports/commits-audit.md` |
| README | AC-15 | AR-07 | `reports/readme-check.md` |
| Dependencias | AC-16 | AR-12 | Revisión de archivos |
| Commits | AC-17 | AR-11 | `reports/commits-audit.md` |
| Swagger | AC-18 | AR-06 | `/api/docs/` |
| Producto completo | AC-19 | AR-01…AR-05 | `reports/acceptance-run.md` |
| Defensa individual | AC-20, AC-21 | AR-14, AR-15 | `reports/defense-rehearsal.md` |

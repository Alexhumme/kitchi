# Kitchi Studio

Aplicación web móvil para crear gatos chibi personalizados mediante ilustraciones 2D por capas, generar paquetes de seis stickers PNG transparentes, transformar fotografías con IA y compartir creaciones en un hub comunitario.

**Proyecto final de Programación Avanzada A1 — Universidad de La Guajira · 2026-2**

> **Estado actual:** el **backend** está implementado y en uso: API REST con Django REST Framework, modelo de datos aplicado sobre MySQL 8, cuentas con token y permisos RBAC, validación contra catálogo, consola de administración (`http://127.0.0.1:8000/admin/`) y documentación OpenAPI/Swagger (`http://127.0.0.1:8000/api/docs/`). La **interfaz Flet Web ya está implementada** y consume la API para catálogo, poses, registro, login, sesión y CRUD de gatos; el editor muestra una **previsualización provisional con placeholders de color** porque la diseñadora aún no entregó los assets definitivos. El **motor de composición con Pillow**, la generación/descarga de stickers, el hub y la integración de IA siguen pendientes. El avance real se sigue en [`docs/10_DEVELOPMENT_CHECKLIST.md`](docs/10_DEVELOPMENT_CHECKLIST.md); no se presentan como terminadas las funciones que solo existen en el diseño.

## Problema que resuelve

Crear stickers personalizados suele requerir saber ilustrar o pagar una herramienta de diseño. Kitchi Studio permite que una persona sin conocimientos de dibujo componga un gato chibi a partir de recursos gráficos compatibles, obtenga un paquete de seis stickers con fondo transparente y los comparta o reutilice desde una galería comunitaria.

El valor diferencial es el **motor 2D por capas**: no se producen 729 ilustraciones para las 3⁶ combinaciones, sino un catálogo inicial de 18 opciones (tres por cada uno de los seis campos) que el motor compone de forma determinista. La IA es un diferenciador adicional para transformar una fotografía de referencia, no un requisito para usar el editor.

## Funcionalidades principales

1. **Editor de personajes:** crear un gato y personalizar pelaje, ojos, cabello, parte superior, parte inferior y accesorios. La previsualización usa placeholders de color hasta que existan los assets de diseño.
2. **Cuenta y persistencia:** registrarse, iniciar sesión, mantener la sesión y guardar hasta tres gatos por cuenta; el modo invitado guarda en el almacenamiento del navegador.
3. **Generación y descarga:** generar seis poses y descargar los PNG transparentes. **Pendiente:** requiere el motor Pillow y los endpoints de paquetes.
4. **Comunidad:** publicar una creación, explorarla desde otra sesión y copiarla sin alterar el original. **Pendiente:** requiere los endpoints de publicaciones.
5. **IA (diferenciador):** subir una fotografía, ejecutar una inferencia real, revisar el resultado y continuar el flujo manual si el servicio falla. **Pendiente.**
6. **Programación avanzada (diferenciador):** evidencias reproducibles de concurrencia, multiprocesamiento y paralelismo en la generación de stickers. **Pendiente.**

## Stack

| Capa | Tecnología |
| --- | --- |
| Interfaz | Python + Flet Web (diseño móvil primero) |
| API | Django + Django REST Framework |
| Documentación de API | drf-spectacular (OpenAPI 3 + Swagger UI) |
| Base de datos | MySQL 8 mediante el ORM de Django |
| Motor gráfico | Pillow |
| IA | Adaptador de proveedor o modelo local (decisión en ADR-003) |
| Procesamiento | `asyncio` + `concurrent.futures` |
| Configuración | `python-dotenv` + `.env` |
| Pruebas | pytest / Django TestCase |
| Control de versiones | Git + GitHub |

## Arquitectura en una imagen

```
Flet Web (interfaz)
        │  HTTP/JSON
        ▼
Django REST Framework (API, permisos, validación)
        │
        ├── MySQL (usuarios, gatos, publicaciones, trabajos)
        ├── storage/ (PNG y recursos generados)
        └── Motor Pillow + adaptador de IA (servicios)
```

Detalle completo en [`docs/03_ARCHITECTURE.md`](docs/03_ARCHITECTURE.md). Decisiones en [`docs/decisions/`](docs/decisions/).

## Integrantes

> **Pendiente de completar antes de la entrega (P31/AR-09).** El profesor exige los nombres de todas las personas en el README. No se inventan nombres.

| Nombre | Rol | Responsabilidad principal | Commits |
| --- | --- | --- | --- |
| Martin Solano | Integrante A — Frontend y UX | Flet, navegación, editor, estados, hub | ≥ 5 |
| Alex Valdelamar | Integrante B — Backend y datos | DRF, MySQL, autenticación, permisos, Swagger | ≥ 5 |
| Aixa Claret Gutierrez | Integrante C — | Guía visual, personajes, poses, accesorios, documentación visual | ≥ 5 |

Todos los integrantes deben poder explicar cualquier parte del código durante la sustentación, no solo su módulo.

## Instalación y ejecución

> **Contrato de instalación:** el backend se verificó en este equipo el 4 de noviembre de
> 2026 (Python 3.14.7, Windows, MySQL 8.0.45) y dejó evidencia en
> [`docs/reports/week1-validation.md`](docs/reports/week1-validation.md). El frontend Flet
> y la integración se ejecutaron con Python 3.11.6 el 9 de noviembre de 2026; sus pruebas
> están registradas en [`docs/reports/frontend-integration.md`](docs/reports/frontend-integration.md).
> La validación completa desde un clon limpio sigue correspondiendo a la tarea P29.

### Requisitos previos

- **Python 3.14.7** para el backend (versión con la que se fijó `backend/requirements.txt`;
  el entorno de este equipo está en 3.11.6 y las 47 pruebas también pasan).
- **Python 3.11+** para el frontend Flet (`frontend/pyproject.toml`); verificado con 3.11.6.
- MySQL 8 en local (verificado con 8.0.45). Si tu equipo no puede instalarlo, arranca con
  `DB_ENGINE=sqlite` en `.env` — el modelo de datos y las migraciones no cambian ([ADR-005](docs/decisions/ADR-005-autenticacion-y-rbac.md)).
- Git.
- PowerShell, Bash o una terminal equivalente.

### 1. Clonar el repositorio

```bash
git clone https://github.com/Alexhumme/kitchi.git
cd kitchi
```

### 2. Crear el entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En Bash:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Configurar variables de entorno

```powershell
Copy-Item .env.example .env
```

Editar `.env` con las credenciales locales de MySQL y la clave de Django. **Nunca** commitear `.env`.

### 4. Instalar dependencias

```bash
pip install -r backend/requirements.txt
```

Verificado: 10 paquetes con versiones fijadas en `backend/requirements.txt` (tarea P32). El
driver de MySQL es **PyMySQL**, porque `mysqlclient` no publica ruedas para Python 3.14 y
obligaría a instalar un compilador en cada equipo.

Instala el frontend (Flet Web y herramientas de prueba):

```bash
pip install -e "frontend[dev]"
```

El frontend declara `flet[web]==1.1.2` y `requires-python = ">=3.11"` en
[`frontend/pyproject.toml`](frontend/pyproject.toml). Si usas un Python distinto al del
backend, instala el frontend en su propio entorno o con `python -m pip` del intérprete 3.11.

### 5. Preparar la base de datos

```bash
python backend/manage.py migrate
python backend/manage.py createsuperuser   # cuenta para la consola /admin/
```

Verificado contra MySQL 8.0.45: seis migraciones de dominio, 19 tablas creadas. Requiere una
`.env` con `DB_*` correctos. La consola de administración gestiona cuentas, catálogo, poses,
gatos, paquetes, publicaciones y trabajos; su funcionamiento se explica en la
[guía viva, sección 5.1](docs/12_GUIA_PLATAFORMA.md).

El catálogo real de assets todavía no existe (P06), pero la API necesita opciones para que
el editor funcione. Siembra las 18 opciones y 6 poses provisionales (idempotente):

```bash
python scripts/seed_catalog.py
```

El script usa las rutas `assets/placeholders/...`; no crea imágenes. Las opciones y poses
quedan activas en MySQL y `/api/catalog/` y `/api/poses/` ya las devuelven.
`scripts/seed_demo_data.py` sigue siendo un marcador sin implementar (tarea P26); no lo
ejecutes todavía.

### 6. Iniciar backend y frontend

```bash
python backend/manage.py runserver 127.0.0.1:8000
```

- API: `http://127.0.0.1:8000/api/health/` → `{"status":"ok","database":"up","engine":"mysql"}`
- Swagger: `http://127.0.0.1:8000/api/docs/` (verificado, 9 endpoints)
- Esquema OpenAPI: `http://127.0.0.1:8000/api/schema/` (verificado)
- Consola de administración: `http://127.0.0.1:8000/admin/` (verificado, 9 entidades)

Con el backend en marcha, levanta la interfaz Flet en otra terminal:

```bash
flet run frontend/src/main.py --web --port 8550
```

- Interfaz: `http://127.0.0.1:8550/`
- El cliente lee `KITCHI_API_URL`, luego `API_BASE_URL` (entorno o `.env` de la raíz). Sin
  URL, entra en **modo local**: la interfaz de invitado funciona con almacenamiento del
  navegador, sin llamadas a la API.
- La pantalla **Perfil** muestra si la API está conectada, el origen del catálogo y los
  datos de la sesión. Los estados de error de login, registro y guardado se muestran en
  línea o como SnackBar.

### 7. Pruebas y benchmark

```bash
cd backend && python -m pytest
```

Verificado: 47 pruebas en verde, incluidas las de la consola de administración. Usan SQLite en
memoria porque el usuario de desarrollo de MySQL no tiene privilegio `CREATE DATABASE`; la
verificación sobre MySQL real se hace con el servidor en marcha:

```bash
python scripts/check_backend.py
```

Verificado: 19 comprobaciones del flujo de cuentas, catálogo y gatos, con limpieza automática
de sus propios datos. `scripts/benchmark_generation.py` sigue siendo un marcador sin
implementar (tareas P22/P27).

Pruebas del frontend:

```bash
python -m pytest -q frontend/tests
```

Verificado: **34 pruebas en verde** (cliente HTTP, catálogo, almacenamiento de invitado y
sesión, modelos y adaptación de la configuración del backend). El 9 de noviembre también se
construyeron todas las pantallas con un `FakeApp` para comprobar que los controles Flet se
crean sin errores; el resultado está en
[`docs/reports/frontend-integration.md`](docs/reports/frontend-integration.md). No se ha
hecho todavía una prueba manual completa en navegador desde un clon limpio.

Los comandos exactos y los resultados se registran en [`docs/reports/`](docs/reports/).

## Uso de IA

La rúbrica permite usar IA, pero exige que cada integrante entienda el código y que el README declare las herramientas. Esta sección se actualiza durante el desarrollo.

| Herramienta | Para qué se usó | Partes del proyecto |
| --- | --- | --- |
| OpenCode (agente de IA) | Análisis del PDF del curso, revisión de la documentación, redacción y adecuación de la rúbrica | `docs/00`–`docs/13`, `README.md`, `AGENTS.md` |
| OpenCode (agente de IA) | Integración Flet ↔ API: cliente HTTP, catálogo dinámico, sesión, pantallas de login/perfil, editor con placeholders, ajustes de tests y documentación del incremento. Todo el código se revisó y se ejecutó con pytest y un smoke test de pantallas | `frontend/`, `scripts/seed_catalog.py`, [`docs/reports/frontend-integration.md`](docs/reports/frontend-integration.md) |
| Qoder (agente de IA) | Andamiaje del backend: estructura de apps, modelos y migraciones, permisos RBAC, envoltorio de errores, endpoints de cuentas/catálogo/gatos, pruebas pytest y verificación en vivo sobre MySQL. Todo el código se revisó, se ejecutó y se explica en [`docs/12_GUIA_PLATAFORMA.md`](docs/12_GUIA_PLATAFORMA.md) | `backend/`, `shared/contracts/openapi.yaml`, `scripts/check_backend.py`, [ADR-005](docs/decisions/ADR-005-autenticacion-y-rbac.md) |
| _[Completar por cada integrante]_ | _[Desarrollo, pruebas, revisión, diseño]_ | _[Módulos]_ |

Reglas:

- Ningún integrante presenta código generado por IA que no pueda explicar, modificar o depurar.
- La IA usada para desarrollar se declara por separado de la IA del producto.
- No se pegan claves, tokens, fotografías privadas ni datos de usuarios en herramientas externas.
- Las respuestas de la IA se revisan y se prueban; no se aceptan como evidencia de que una función funciona.

## Documentación

| Documento | Contenido |
| --- | --- |
| [`docs/00_PROJECT_OVERVIEW.md`](docs/00_PROJECT_OVERVIEW.md) | Visión general y objetivo |
| [`docs/01_MASTER_PLAN.md`](docs/01_MASTER_PLAN.md) | Plan de 4 semanas, hitos y riesgos |
| [`docs/02_REQUIREMENTS.md`](docs/02_REQUIREMENTS.md) | Alcance y criterios de aceptación |
| [`docs/03_ARCHITECTURE.md`](docs/03_ARCHITECTURE.md) | Arquitectura, stack y estructura |
| [`docs/04_DATA_MODEL.md`](docs/04_DATA_MODEL.md) | Modelo de datos |
| [`docs/05_API_CONTRACTS.md`](docs/05_API_CONTRACTS.md) | Endpoints y Swagger |
| [`docs/06_DESIGN_SYSTEM.md`](docs/06_DESIGN_SYSTEM.md) | Recursos gráficos y capas |
| [`docs/07_AI_INTEGRATION.md`](docs/07_AI_INTEGRATION.md) | Estrategia de IA |
| [`docs/08_CONCURRENCY_AND_PARALLELISM.md`](docs/08_CONCURRENCY_AND_PARALLELISM.md) | Evidencias de programación avanzada |
| [`docs/09_TEST_PLAN.md`](docs/09_TEST_PLAN.md) | Plan de pruebas |
| [`docs/10_DEVELOPMENT_CHECKLIST.md`](docs/10_DEVELOPMENT_CHECKLIST.md) | Tablero P01–P40 |
| [`docs/11_DEMO_SCRIPT.md`](docs/11_DEMO_SCRIPT.md) | Guion de 10 minutos |
| [`docs/12_GUIA_PLATAFORMA.md`](docs/12_GUIA_PLATAFORMA.md) | Guía viva para la sustentación |
| [`docs/13_CUMPLIMIENTO_ACADEMICO.md`](docs/13_CUMPLIMIENTO_ACADEMICO.md) | Rúbrica y checklist de entrega |
| [`AGENTS.md`](AGENTS.md) | Reglas para agentes e integrantes |

## Repositorio y commits

- Repositorio: <https://github.com/Alexhumme/kitchi>
- Mínimo **5 commits descriptivos por integrante**.
- Ramas por funcionalidad y revisión cruzada antes de integrar.
- `.gitignore` excluye `.env`, `__pycache__`, bases locales y temporales.
- No se versionan secretos, tokens, contraseñas ni fotografías privadas.
- Antes de la entrega se ejecuta la auditoría de [`docs/reports/academic-audit.md`](docs/reports/academic-audit.md).

## Demostración

- Fecha límite: **miércoles 25 de noviembre de 2026, 12:00 m. (hora Colombia)**.
- Sustentación: **10 minutos** por grupo (demo en vivo + preguntas individuales).
- Guion: [`docs/11_DEMO_SCRIPT.md`](docs/11_DEMO_SCRIPT.md).
- Preparación individual: [`docs/12_GUIA_PLATAFORMA.md`](docs/12_GUIA_PLATAFORMA.md).

## Reglas para agentes de programación

Ver [`AGENTS.md`](AGENTS.md). Resumen: leer la documentación obligatoria antes de editar, no cambiar contratos compartidos sin coordinación, registrar decisiones en `docs/decisions/`, actualizar la guía viva en cada incremento y no marcar tareas como terminadas sin evidencia.

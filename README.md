# Kitchi Studio

Aplicación web móvil para crear gatos chibi personalizados mediante ilustraciones 2D por capas, generar paquetes de seis stickers PNG transparentes, transformar fotografías con IA y compartir creaciones en un hub comunitario.

**Proyecto final de Programación Avanzada A1 — Universidad de La Guajira · 2026-2**

> **Estado actual:** documentación, arquitectura y plan de 4 semanas listos. El código de la aplicación aún no está implementado; el avance real se sigue en [`docs/10_DEVELOPMENT_CHECKLIST.md`](docs/10_DEVELOPMENT_CHECKLIST.md). No se presentan como terminadas las funciones que solo existen en el diseño.

## Problema que resuelve

Crear stickers personalizados suele requerir saber ilustrar o pagar una herramienta de diseño. Kitchi Studio permite que una persona sin conocimientos de dibujo componga un gato chibi a partir de recursos gráficos compatibles, obtenga un paquete de seis stickers con fondo transparente y los comparta o reutilice desde una galería comunitaria.

El valor diferencial es el **motor 2D por capas**: no se producen 729 ilustraciones para las 3⁶ combinaciones, sino un catálogo inicial de 18 opciones (tres por cada uno de los seis campos) que el motor compone de forma determinista. La IA es un diferenciador adicional para transformar una fotografía de referencia, no un requisito para usar el editor.

## Funcionalidades principales

1. **Editor de personajes:** crear un gato y personalizar pelaje, ojos, cabello, parte superior, parte inferior y accesorios.
2. **Generación y descarga:** generar seis poses y descargar los PNG transparentes.
3. **Cuenta y comunidad:** registrarse, iniciar sesión, publicar una creación, explorarla desde otra sesión y copiarla sin alterar el original.
4. **IA (diferenciador):** subir una fotografía, ejecutar una inferencia real, revisar el resultado y continuar el flujo manual si el servicio falla.
5. **Programación avanzada (diferenciador):** evidencias reproducibles de concurrencia, multiprocesamiento y paralelismo en la generación de stickers.

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

> **Contrato de instalación:** los comandos siguientes se validarán desde un clon limpio en la tarea P29 y se corregirán aquí. Mientras el código no exista, esta sección describe la instalación prevista; no es una promesa de que ya funcione.

### Requisitos previos

- Python 3.12 o superior (versión exacta por fijar en P02).
- MySQL 8 en local (o la alternativa que se apruebe en un ADR).
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
pip install -e frontend
```

Las versiones se fijan en `backend/requirements.txt` y `frontend/pyproject.toml` (tarea P32). Si el equipo opta por un único archivo, se documentará aquí.

### 5. Preparar la base de datos

```bash
python backend/manage.py migrate
python scripts/seed_demo_data.py
```

`seed_demo_data.py` debe ser idempotente y no requiere editar la base de datos a mano.

### 6. Iniciar backend y frontend

En una terminal:

```bash
python backend/manage.py runserver
```

En otra terminal:

```bash
flet run frontend/src/main.py --web --port 8550
```

- API: `http://127.0.0.1:8000/`
- Swagger: `http://127.0.0.1:8000/api/docs/`
- Esquema OpenAPI: `http://127.0.0.1:8000/api/schema/`
- Interfaz: `http://127.0.0.1:8550/`

### 7. Pruebas y benchmark

```bash
pytest
python scripts/benchmark_generation.py
```

Los comandos exactos y los resultados se registran en [`docs/reports/`](docs/reports/).

## Uso de IA

La rúbrica permite usar IA, pero exige que cada integrante entienda el código y que el README declare las herramientas. Esta sección se actualiza durante el desarrollo.

| Herramienta | Para qué se usó | Partes del proyecto |
| --- | --- | --- |
| OpenCode (agente de IA) | Análisis del PDF del curso, revisión de la documentación, redacción y adecuación de la rúbrica | `docs/00`–`docs/13`, `README.md`, `AGENTS.md` |
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

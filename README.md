# Kitchi Studio

Aplicación web móvil para crear gatos chibi personalizados mediante ilustraciones 2D por capas, generar paquetes de seis stickers PNG transparentes, transformar fotografías con IA y compartir creaciones en un hub comunitario.

**Proyecto final de Programación Avanzada A1 — Universidad de La Guajira · 2026-2**

> **Estado actual:** el **backend** está implementado y en uso: API REST con Django REST Framework, modelo de datos aplicado sobre MySQL 8, cuentas con token y permisos RBAC, validación contra catálogo, consola de administración (`http://127.0.0.1:8000/admin/`) y documentación OpenAPI/Swagger (`http://127.0.0.1:8000/api/docs/`). La **interfaz React** es la única interfaz activa y usa los SVG reales de cuerpo, cabello dividido, prendas y accesorios, con sliders de color, previews reales y multiaccesorio. El **hub de publicaciones** está implementado. El **motor Pillow**, la generación/descarga de stickers, la copia de publicaciones y la integración de IA siguen pendientes. El avance real se sigue en [`docs/10_DEVELOPMENT_CHECKLIST.md`](docs/10_DEVELOPMENT_CHECKLIST.md); no se presentan como terminadas las funciones que solo existen en el diseño.

## Problema que resuelve

Crear stickers personalizados suele requerir saber ilustrar o pagar una herramienta de diseño. Kitchi Studio permite que una persona sin conocimientos de dibujo componga un gato chibi a partir de recursos gráficos compatibles, obtenga un paquete de seis stickers con fondo transparente y los comparta o reutilice desde una galería comunitaria.

El valor diferencial es el **motor 2D por capas**: no se producen todas las combinaciones como imágenes independientes, sino un catálogo de recursos que el motor compone de forma determinista. El catálogo actual tiene 53 códigos, incluidos aliases de clientes antiguos, y seis poses; las 18 opciones fueron el inventario conceptual inicial. La IA es un diferenciador adicional para transformar una fotografía de referencia, no un requisito para usar el editor.

## Funcionalidades principales

1. **Editor de personajes:** crear un gato y personalizar pelaje, ojos, cabello, parte superior, parte inferior y accesorios. La interfaz usa SVG reales, cabello delantero/trasero, sliders de color, un mini slider por accesorio seleccionado, previews por opción y varios accesorios sin repetir su tipo. La cabeza se dibuja delante de la prenda superior para que los cuellos queden detrás.
2. **Cuenta y persistencia:** registrarse, iniciar sesión, mantener la sesión y guardar hasta tres gatos por cuenta; el modo invitado guarda en el almacenamiento del navegador.
3. **Generación y descarga:** generar seis poses y descargar los PNG transparentes. **Pendiente:** requiere el motor Pillow y los endpoints de paquetes.
4. **Comunidad:** publicar una creación, explorarla desde otra sesión y consultar perfiles públicos. **Implementado:** feed, buscador, publicación y perfil. **Pendiente:** copiar una creación sin alterar el original (P19).
5. **IA (diferenciador):** subir una fotografía, ejecutar una inferencia real, revisar el resultado y continuar el flujo manual si el servicio falla. **Pendiente.**
6. **Programación avanzada (diferenciador):** evidencias reproducibles de concurrencia, multiprocesamiento y paralelismo en la generación de stickers. **Pendiente.**

## Stack

| Capa | Tecnología |
| --- | --- |
| Interfaz | React 19 + TypeScript + Vite, con SVG reales y CSS propio |
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
React 19 + Vite (interfaz web) ──→ HTTP/JSON → Django REST Framework
                                              │
                                              ├── MySQL
                                              ├── storage/
                                              └── Pillow + IA (pendiente)
```

Detalle completo en [`docs/03_ARCHITECTURE.md`](docs/03_ARCHITECTURE.md). Decisiones en [`docs/decisions/`](docs/decisions/).

## Integrantes

> **Pendiente de completar antes de la entrega (P31/AR-09).** El profesor exige los nombres de todas las personas en el README. No se inventan nombres.

| Nombre | Rol | Responsabilidad principal | Commits |
| --- | --- | --- | --- |
| Martin Solano | Integrante A — Frontend y UX | React, navegación, editor, estados, hub | ≥ 5 |
| Alex Valdelamar | Integrante B — Backend y datos | DRF, MySQL, autenticación, permisos, Swagger | ≥ 5 |
| Aixa Claret Gutierrez | Integrante C — | Guía visual, personajes, poses, accesorios, documentación visual | ≥ 5 |

Todos los integrantes deben poder explicar cualquier parte del código durante la sustentación, no solo su módulo.

## Instalación y ejecución

> **Contrato de instalación:** el backend se verificó en este equipo el 4 de noviembre de
> 2026 (Python 3.14.7, Windows, MySQL 8.0.45) y dejó evidencia en
> [`docs/reports/week1-validation.md`](docs/reports/week1-validation.md). React se verificó con Node 24.22.1 y npm 11.19.0 el 23 de noviembre de 2026; su evidencia está en [`docs/reports/frontend-react.md`](docs/reports/frontend-react.md).
> La validación completa desde un clon limpio sigue correspondiendo a la tarea P29.

### Requisitos previos

- **Python 3.14.7** para el backend (versión con la que se fijó `backend/requirements.txt`;
  las pruebas del backend se ejecutaron con Python 3.11.6 y las 66 pruebas pasan).
- **Node.js 20+ y npm 10+** para la interfaz React; verificado con Node 24.22.1 y npm 11.19.0.
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

Instala la interfaz React:

```bash
cd frontend-react
npm install
```

Las dependencias y sus versiones están fijadas en [`frontend-react/package.json`](frontend-react/package.json) y `frontend-react/package-lock.json`.

### 5. Preparar la base de datos

```bash
python backend/manage.py migrate
python backend/manage.py createsuperuser   # cuenta para la consola /admin/
```

Verificado contra MySQL 8.0.45: seis migraciones de dominio, 19 tablas creadas. Requiere una
`.env` con `DB_*` correctos. La consola de administración gestiona cuentas, catálogo, poses,
gatos, paquetes, publicaciones y trabajos; su funcionamiento se explica en la
[guía viva, sección 5.1](docs/12_GUIA_PLATAFORMA.md).

Siembra el catálogo real con **53 opciones** —recursos SVG y aliases de compatibilidad— y
**6 poses**. El script es idempotente:

```bash
python scripts/seed_catalog.py
```

El catálogo incluye rutas reales de los SVG y los grupos de compatibilidad de accesorios.
La API los devuelve desde `/api/catalog/` y `/api/poses/`. La autoría y aprobación visual
siguen registrándose en `assets/catalog.json` (P06/P08). `scripts/seed_demo_data.py` sigue
siendo un marcador sin implementar (tarea P26); no lo ejecutes todavía.

### 6. Iniciar backend y frontend

```bash
python backend/manage.py runserver 127.0.0.1:8000
```

- API: `http://127.0.0.1:8000/api/health/` → `{"status":"ok","database":"up","engine":"mysql"}`
- Swagger: `http://127.0.0.1:8000/api/docs/` (contrato vigente: 12 rutas y 16 operaciones)
- Esquema OpenAPI: `http://127.0.0.1:8000/api/schema/` (verificado)
- Consola de administración: `http://127.0.0.1:8000/admin/` (verificado, 9 entidades)

Con el backend en marcha, levanta la interfaz React en otra terminal:

```bash
cd frontend-react
npm run dev
```

- Interfaz: `http://127.0.0.1:5173/`.
- El backend permite los orígenes 5173/4173 por defecto. Si defines `CORS_ALLOWED_ORIGINS`, añade manualmente los orígenes que uses.
- Para otro backend, define `VITE_API_URL` antes de arrancar o en `frontend-react/.env.local` (ese archivo no se versiona).
- El modo invitado guarda en `localStorage`; con sesión usa `/api/cats/` y conserva el token de Django.
- La pantalla **Perfil** permite crear una cuenta, iniciar/cerrar sesión y consultar el estado de la API.
- Build de producción: `cd frontend-react && npm run build`; preview local: `npm run preview`.

### 7. Pruebas y benchmark

```bash
cd backend && python -m pytest
```

Verificado: **66 pruebas en verde**, incluidas las de la consola de administración y la
validación de colores independientes en accesorios múltiples. Usan SQLite en memoria porque el usuario de
desarrollo de MySQL no tiene privilegio `CREATE DATABASE`; la verificación sobre MySQL real
se hace con el servidor en marcha:

```bash
python scripts/check_backend.py
```

Verificado: 19 comprobaciones del flujo de cuentas, catálogo y gatos, con limpieza automática
de sus propios datos. `scripts/benchmark_generation.py` sigue siendo un marcador sin
implementar (tareas P22/P27).

Pruebas de la interfaz:

```bash
cd frontend-react
npm run build
npm run lint
```

Verificado el 23 de noviembre: build correcto y lint con **0 errores y 2 avisos** conocidos `set-state-in-effect`. Las 46 pruebas Flet son históricas; la carpeta y sus pruebas se retiraron al adoptar React como interfaz definitiva ([ADR-011](docs/decisions/ADR-011-react-interfaz-definitiva.md)).

Los comandos exactos y los resultados se registran en [`docs/reports/`](docs/reports/).

## Uso de IA

La rúbrica permite usar IA, pero exige que cada integrante entienda el código y que el README declare las herramientas. Esta sección se actualiza durante el desarrollo.

| Herramienta | Para qué se usó | Partes del proyecto |
| --- | --- | --- |
| OpenCode (agente de IA) | Análisis del PDF del curso, revisión de la documentación, redacción y adecuación de la rúbrica | `docs/00`–`docs/13`, `README.md`, `AGENTS.md` |
| OpenCode (agente de IA) | Integración Flet ↔ API: cliente HTTP, catálogo dinámico, sesión, pantallas de login/perfil, editor con placeholders, ajustes de tests y documentación del incremento. Todo el código se revisó y se ejecutó con pytest y un smoke test de pantallas | `frontend/`, `scripts/seed_catalog.py`, [`docs/reports/frontend-integration.md`](docs/reports/frontend-integration.md) |
| Qoder (agente de IA) | Andamiaje del backend: estructura de apps, modelos y migraciones, permisos RBAC, envoltorio de errores, endpoints de cuentas/catálogo/gatos, pruebas pytest y verificación en vivo sobre MySQL. Todo el código se revisó, se ejecutó y se explica en [`docs/12_GUIA_PLATAFORMA.md`](docs/12_GUIA_PLATAFORMA.md) | `backend/`, `shared/contracts/openapi.yaml`, `scripts/check_backend.py`, [ADR-005](docs/decisions/ADR-005-autenticacion-y-rbac.md) |
| Qoder (agente de IA) | Integración del editor visual con los SVG reales: capas de cabello delantero/trasero, cabeza delantera sobre la ropa, sliders HSL, previews compartidas, multiaccesorio, persistencia y compatibilidad legacy. Se verificaron build, lint, backend, OpenAPI e interacción en navegador y MySQL; la evidencia y las limitaciones están en [`docs/reports/editor-visual-assets.md`](docs/reports/editor-visual-assets.md) | `frontend-react/`, `backend/apps/catalog/`, `backend/tests/`, `scripts/seed_catalog.py`, `shared/contracts/openapi.yaml`, [ADR-010](docs/decisions/ADR-010-configuracion-visual-compatible.md) |
| Qoder (agente de IA) | Adopción de React como interfaz definitiva, retirada de Flet y alineación de instalación, arquitectura, guía viva y evidencia | `frontend-react/`, `README.md`, `docs/`, [ADR-011](docs/decisions/ADR-011-react-interfaz-definitiva.md) |
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

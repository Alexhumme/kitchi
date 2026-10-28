# 03 · Arquitectura — Kitchi Studio

Arquitectura lógica, tecnologías, estructura del repositorio y calidad técnica · Versión 1.1 · 28 de octubre de 2026

> Decisiones de arquitectura registradas en [`decisions/`](decisions/). No cambiar la arquitectura, el esquema de datos, los contratos de API ni las dependencias principales sin un ADR previo. La adecuación a la rúbrica del curso está en [ADR-004](decisions/ADR-004-academic-requirements.md).

## Decisión arquitectónica de base

Se conserva Python, Flet, Django REST Framework y MySQL, con una distinción importante:

- **Flet** será la interfaz web móvil.
- **Django REST Framework** será la API del sistema.
- **MySQL** será la persistencia relacional.
- **Pillow** será el motor de composición 2D.
- **drf-spectacular** generará la documentación OpenAPI/Swagger.

No se recomienda crear dos backends, repartir la lógica entre Flet y Django, ni introducir microservicios o infraestructura compleja. La propuesta se apoya en librerías conocidas y evita una cola de mensajes o un servidor de tareas independiente durante la primera versión.

El PDF del curso no impone un stack concreto; esta arquitectura cumple el requisito de aplicación real con interfaz, API, base de datos y documentación automática. MySQL es el motor elegido; SQLite o PostgreSQL son alternativas válidas si un ADR de contingencia lo justifica.

## Arquitectura lógica

### Capa 1 — Interfaz Flet

Editor · Selector de poses · Hub · Login · Descargas · Estados de error y carga

### Capa 2 — Django REST Framework

API REST · Validación · Autorización · Reglas de negocio · OpenAPI/Swagger · Tareas

- **MySQL:** usuarios, gatos, publicaciones, paquetes y trabajos.
- **Almacenamiento de archivos:** PNG, referencias y recursos gráficos (sistema de archivos local durante la demostración).

### Capa 3 — Motor de generación

Pillow · asyncio · procesos trabajadores · adaptador de IA

## Responsabilidad de cada tecnología

| Tecnología | Responsabilidad |
| --- | --- |
| Python | Lenguaje principal y lógica del motor gráfico |
| Flet | Interfaz web móvil y controles del editor |
| Django | Backend, modelos, autenticación y reglas de negocio |
| Django REST Framework | API consumida por la interfaz |
| drf-spectacular | Esquema OpenAPI y Swagger UI |
| MySQL | Persistencia relacional |
| python-dotenv | Carga de configuración y secretos desde `.env` |
| Pillow | Composición, transformación y exportación de imágenes |
| `asyncio` | Coordinación asíncrona de operaciones de E/S |
| `concurrent.futures` | Ejecución en hilos o procesos, según el tipo de tarea |
| Servicio de IA o modelo preentrenado | Transformación de fotografías |
| pytest | Pruebas unitarias y de integración |
| Git y repositorio compartido | Integración, revisión y trazabilidad del desarrollo |

## Diseño integrado del flujo de generación

```
Solicitud de generación
        │
Validar configuración y crear registro de trabajo
        │
Coordinador de tareas  ──►  Estado, concurrencia limitada y seguimiento
        │
   ┌────┴────────────────┐
   │                     │
E/S asíncrona      Procesos trabajadores
(IA, red)          (composición y exportación)
   │                     │
   └────┬────────────────┘
        ▼
Resultado: seis PNG · estado completado o fallido · métricas de ejecución
```

Detalle de los casos de uso de concurrencia en [08_CONCURRENCY_AND_PARALLELISM.md](08_CONCURRENCY_AND_PARALLELISM.md).

## Documentación de la API

- `GET /api/schema/` — esquema OpenAPI 3 generado por drf-spectacular.
- `GET /api/docs/` — Swagger UI navegable.
- `GET /api/health/` — verificación básica de disponibilidad.
- Los contratos compartidos se versionan en `shared/contracts/`.
- La API debe poder demostrarse desde Swagger sin depender de la interfaz Flet.

Swagger/OpenAPI es un requisito académico (AR-06 / AC-18) y también una herramienta de trabajo para frontend y backend en paralelo.

## Condiciones que validan la arquitectura (semana 1)

Ver antes [01_MASTER_PLAN.md](01_MASTER_PLAN.md#condiciones-técnicas-que-deben-verificarse-en-la-semana-1). Los resultados se documentan en [`reports/`](reports/) y las decisiones derivadas en [`decisions/`](decisions/).

## Estructura del repositorio

```
kitchi/
├── README.md
├── AGENTS.md
├── .gitignore
├── .env.example
├── docker-compose.yml              # Opcional, solo si se acuerda usarlo
├── docs/
│   ├── 00_PROJECT_OVERVIEW.md
│   ├── 01_MASTER_PLAN.md
│   ├── 02_REQUIREMENTS.md
│   ├── 03_ARCHITECTURE.md
│   ├── 04_DATA_MODEL.md
│   ├── 05_API_CONTRACTS.md
│   ├── 06_DESIGN_SYSTEM.md
│   ├── 07_AI_INTEGRATION.md
│   ├── 08_CONCURRENCY_AND_PARALLELISM.md
│   ├── 09_TEST_PLAN.md
│   ├── 10_DEVELOPMENT_CHECKLIST.md
│   ├── 11_DEMO_SCRIPT.md
│   ├── 12_GUIA_PLATAFORMA.md
│   ├── 13_CUMPLIMIENTO_ACADEMICO.md
│   ├── Proyecto-final-Programacion-Avanzada-A1-20262.pdf
│   ├── decisions/
│   │   ├── ADR-001-frontend-backend.md
│   │   ├── ADR-002-character-rendering.md
│   │   ├── ADR-003-ai-strategy.md
│   │   └── ADR-004-academic-requirements.md
│   └── reports/
├── frontend/
│   ├── pyproject.toml
│   ├── src/
│   └── tests/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   ├── apps/
│   │   ├── accounts/
│   │   ├── catalog/
│   │   ├── cats/
│   │   ├── stickers/
│   │   ├── community/
│   │   └── ai_jobs/
│   └── tests/
├── shared/
│   └── contracts/
├── assets/
│   ├── characters/
│   ├── poses/
│   ├── ui/
│   └── catalog.json
├── storage/
│   └── .gitkeep
└── scripts/
    ├── setup_dev.py
    ├── seed_demo_data.py
    └── benchmark_generation.py
```

Notas:

- La estructura es orientativa. No es obligatorio separar cada entidad en una aplicación Django diferente si el código resultante es demasiado pequeño, pero la separación por dominio debe ser clara.
- `frontend/src/` y `backend/apps/` se adaptan al empaquetado real que se escoja.
- `docker-compose.yml` queda opcional: no se introduce Docker si el equipo no lo domina o su configuración consume tiempo necesario para las funcionalidades.
- `backend/requirements.txt` y `frontend/pyproject.toml` deben fijar versiones verificadas antes de la entrega. Si se prefiere, un único `requirements.txt` en la raíz es aceptable para la rúbrica.
- `storage/` y `.env` nunca se versionan.

## Calidad técnica del código

La rúbrica evalúa código limpio, organizado por módulos o apps, uso correcto del framework, variables descriptivas, separación de lógica y presentación, `.env` para secretos y ausencia de código muerto. Reglas del proyecto:

- Una app Django por dominio (`accounts`, `catalog`, `cats`, `stickers`, `community`, `ai_jobs`).
- Modelos, serializers, vistas y servicios con responsabilidades separadas.
- La lógica de composición y la lógica de IA viven en servicios/módulos, no en las vistas.
- Las vistas orquestan; no contienen reglas de negocio duplicadas del frontend.
- Nombres descriptivos en español o inglés consistente; no abreviaturas crípticas.
- Sin código comentado, archivos vacíos ni funciones sin uso al cerrar la entrega.
- Configuración por variables de entorno; ningún secreto hardcodeado.
- Pruebas automatizadas para límites, permisos, estados y composición.
- Revisión cruzada antes de fusionar; ningún integrante fusiona su propio cambio sin revisión.
- Documentación actualizada y guía viva de la plataforma en cada incremento.

## Repositorio y reproducibilidad

- Repositorio público en GitHub: `https://github.com/Alexhumme/kitchi` (verificar visibilidad antes de la entrega).
- Mínimo 5 commits descriptivos por integrante, incluida la diseñadora.
- `.gitignore` sin `.env`, `__pycache__`, bases locales ni temporales.
- `requirements.txt` o `pyproject.toml` con versiones fijadas.
- README con instalación y ejecución verificadas desde un clon limpio.
- Sin secretos, tokens, contraseñas ni fotografías privadas en el historial.
- La instalación se valida en la tarea P29 y se registra en [`reports/clean-install.md`](reports/clean-install.md).

## Trabajo paralelo con agentes e integrantes

Reglas operativas:

- Una rama Git por funcionalidad.
- Commits pequeños y descriptivos.
- Pull request o revisión cruzada antes de integrar.
- Contratos de API acordados antes de desarrollar frontend y backend en paralelo.
- Pruebas automáticas antes de fusionar cambios.
- Un único responsable de aprobar migraciones y cambios arquitectónicos.
- Ningún agente puede sobrescribir silenciosamente cambios de otro integrante.

Para tres integrantes de desarrollo y una diseñadora: dividir las tareas por componentes y asignar un responsable de integración. No permitir que varios agentes modifiquen simultáneamente los mismos modelos, contratos o archivos de configuración. La documentación y los contratos compartidos son más importantes que la cantidad de agentes utilizados. La diseñadora también debe registrar commits propios (recursos, guía visual, documentación) para cumplir la rúbrica.

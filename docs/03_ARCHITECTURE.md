# 03 · Arquitectura — Kitchi Studio

Arquitectura lógica, tecnologías y estructura del repositorio · Versión 1.0

> Decisiones de arquitectura registradas en [`decisions/`](decisions/). No cambiar la arquitectura, el esquema de datos, los contratos de API ni las dependencias principales sin un ADR previo.

## Decisión arquitectónica de base

Se conserva Python, Flet, Django y MySQL, con una distinción importante:

- **Flet** será la interfaz del prototipo web.
- **Django REST Framework** será la API del sistema.

No se recomienda crear dos backends, repartir la lógica entre Flet y Django, ni introducir microservicios o infraestructura compleja. La propuesta se apoya en librerías conocidas y evita una cola de mensajes o un servidor de tareas independiente durante la primera versión.

## Arquitectura lógica

### Capa 1 — Interfaz Flet

Editor · Selector de poses · Hub · Login · Descargas

### Capa 2 — Django REST Framework

API REST · Validación · Autorización · Reglas de negocio · Tareas

- **MySQL:** usuarios y metadatos.
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
| MySQL | Persistencia relacional |
| Pillow | Composición, transformación y exportación de imágenes |
| `asyncio` | Coordinación asíncrona de operaciones de E/S |
| `concurrent.futures` | Ejecución en hilos o procesos, según el tipo de tarea |
| Servicio de IA o modelo preentrenado | Transformación de fotografías |
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

## Condiciones que validan la arquitectura (semana 1)

Ver antes [01_MASTER_PLAN.md](01_MASTER_PLAN.md#condiciones-técnicas-que-deben-verificarse-en-la-semana-1). Los resultados se documentan en [`reports/`](reports/) y las decisiones derivadas en [`decisions/`](decisions/).

## Estructura del repositorio

```
kitchi-studio/
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
│   ├── decisions/
│   │   ├── ADR-001-frontend-backend.md
│   │   ├── ADR-002-character-rendering.md
│   │   └── ADR-003-ai-strategy.md
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

- La estructura es orientativa. No es obligatorio separar cada entidad en una aplicación Django diferente si el código resultante es demasiado pequeño.
- `frontend/src/` y `backend/apps/` se adaptan al empaquetado real que se escoja.
- `docker-compose.yml` queda opcional: no se introduce Docker si el equipo no lo domina o su configuración consume tiempo necesario para las funcionalidades.

## Trabajo paralelo con agentes e integrantes

Reglas operativas:

- Una rama Git por funcionalidad.
- Commits pequeños y descriptivos.
- Pull request o revisión cruzada antes de integrar.
- Contratos de API acordados antes de desarrollar frontend y backend en paralelo.
- Pruebas automáticas antes de fusionar cambios.
- Un único responsable de aprobar migraciones y cambios arquitectónicos.
- Ningún agente puede sobrescribir silenciosamente cambios de otro integrante.

Para tres integrantes: dividir las tareas por componentes y asignar un responsable de integración. No permitir que varios agentes modifiquen simultáneamente los mismos modelos, contratos o archivos de configuración. La documentación y los contratos compartidos son más importantes que la cantidad de agentes utilizados.

# Kitchi Studio

Aplicación web móvil para crear gatos chibi personalizados mediante ilustraciones 2D por capas, generar paquetes de seis stickers PNG transparentes, transformar fotografías con IA y compartir creaciones en un hub comunitario.

MVP académico · 5 semanas · Python + Flet + Django REST Framework + MySQL

> **Estado actual:** estructura documental creada a partir del [plan maestro](project.md). El código aún no existe; las tareas y su estado se siguen en [docs/10_DEVELOPMENT_CHECKLIST.md](docs/10_DEVELOPMENT_CHECKLIST.md).

## Por dónde empezar

| Soy… | Empieza por |
| --- | --- |
| Integrante nuevo o agente de programación | [AGENTS.md](AGENTS.md) → [docs/00_PROJECT_OVERVIEW.md](docs/00_PROJECT_OVERVIEW.md) |
| Responsable de frontend | [docs/05_API_CONTRACTS.md](docs/05_API_CONTRACTS.md) · [docs/02_REQUIREMENTS.md](docs/02_REQUIREMENTS.md) |
| Responsable de backend | [docs/04_DATA_MODEL.md](docs/04_DATA_MODEL.md) · [docs/05_API_CONTRACTS.md](docs/05_API_CONTRACTS.md) |
| Responsable del motor gráfico / IA / concurrencia | [docs/06_DESIGN_SYSTEM.md](docs/06_DESIGN_SYSTEM.md) · [docs/07_AI_INTEGRATION.md](docs/07_AI_INTEGRATION.md) · [docs/08_CONCURRENCY_AND_PARALLELISM.md](docs/08_CONCURRENCY_AND_PARALLELISM.md) |
| Evaluador o profesor | [docs/02_REQUIREMENTS.md](docs/02_REQUIREMENTS.md) · [docs/09_TEST_PLAN.md](docs/09_TEST_PLAN.md) · [docs/reports/](docs/reports/) |

## Estructura del repositorio

```
kitchi-studio/
├── README.md · AGENTS.md · .gitignore · .env.example
├── docs/            # Documentación rectora (00–11), decisiones ADR y reportes
├── frontend/        # Interfaz Flet (pendiente de inicializar)
├── backend/         # Django REST Framework + MySQL (pendiente de inicializar)
├── shared/contracts/# Contratos API compartidos (pendiente, tarea P03)
├── assets/          # Recursos gráficos y catalog.json (pendiente, tarea P06)
├── storage/         # Archivos generados (fuera de Git)
└── scripts/         # setup_dev.py · seed_demo_data.py · benchmark_generation.py
```

## Instalación y ejecución

**Pendiente de completar con comandos verificados** (tareas P02 y P29; requisitos de reproducibilidad en [docs/09_TEST_PLAN.md](docs/09_TEST_PLAN.md#protocolo-de-instalación-reproducible-ac-13)).

Plan provisional:

1. Requisitos: Python (versión por fijar), MySQL local.
2. Copiar `.env.example` → `.env` y completar credenciales locales (nunca commitear `.env`).
3. Backend: `pip install -r backend/requirements.txt` (versiones fijadas tras la semana 1) → migraciones → `python manage.py runserver`.
4. Frontend: `pip install -e frontend` → iniciar la app Flet apuntando a la API.
5. Pruebas y benchmark: comandos por documentar aquí tras verificarlos.

## Reglas para agentes de programación

Ver [AGENTS.md](AGENTS.md). Resumen: leer la documentación obligatoria antes de editar, no cambiar contratos compartidos sin coordinación, registrar decisiones en `docs/decisions/` y no marcar tareas como terminadas sin evidencia.

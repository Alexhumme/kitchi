# Validación técnica de la semana 1

Evidencia de P02 · Estado: **parcial — lado backend validado; lado Flet pendiente** · Fecha: 2026-11-04

> Registrar versiones exactas y resultados reales. No marcar como validado lo que no se ejecutó.

## Entorno

| Elemento | Valor |
| --- | --- |
| Sistema operativo | Windows 10.0.26200 (x64) |
| Python | 3.14.7 |
| Flet | — (sin instalar; comprobación pendiente del lado frontend) |
| Django | 5.2.19 |
| Django REST Framework | 3.18.3 |
| drf-spectacular | 0.30.0 |
| Pillow | 13.0.0 (instalado, sin uso aún) |
| MySQL | 8.0.45 (servidor local, esquema `Kitchi_db`, usuario de desarrollo) |
| Driver MySQL | PyMySQL 1.2.3 con `install_as_MySQLdb()` (decisión en [ADR-005](../decisions/ADR-005-autenticacion-y-rbac.md)) |
| CORS | django-cors-headers 4.9.0, orígenes desde `CORS_ALLOWED_ORIGINS` |
| Pruebas | pytest 9.2.0 + pytest-django 4.14.0 |
| Navegador | — (Swagger probado por HTTP, no con navegador) |

## Comprobaciones

| # | Comprobación | Resultado | Evidencia |
| --- | --- | --- | --- |
| 1 | Flet sirve una vista web móvil | **Pendiente** | Corresponde al Integrante A |
| 2 | Flet consume un endpoint de DRF | **Pendiente** | Corresponde al Integrante A; la API ya responde con token |
| 3 | Django conecta con MySQL | **OK** | `manage.py migrate` aplicó 19 tablas en MySQL 8.0.45; `/api/health/` devolvió `{"status":"ok","database":"up","engine":"mysql"}` |
| 4 | Las migraciones se aplican desde cero | **OK** | `makemigrations` generó 6 migraciones iniciales y `migrate` las aplicó sin errores |
| 5 | Pillow compone un gato con al menos 3 capas | **Pendiente** | Requiere los recursos de la diseñadora (P04/P06) |
| 6 | El PNG resultante conserva transparencia | **Pendiente** | Tarea P14 |
| 7 | `/api/schema/` y `/api/docs/` cargan | **OK** | Ambos respondieron 200; el esquema se versionó en [`shared/contracts/openapi.yaml`](../../shared/contracts/openapi.yaml) con 9 endpoints, 0 errores y 0 advertencias de drf-spectacular |
| 8 | El mecanismo de autenticación elegido funciona entre Flet y Django | **Parcial — OK en Django** | Registro, login, `me`, logout e invalidación de token verificados sobre MySQL; falta la prueba desde el cliente Flet (tarea 2) |

## Verificación del backend (2026-11-04)

Dos niveles de evidencia, ambos ejecutados en este equipo:

1. **Pruebas automatizadas** — `cd backend && python -m pytest`: **47 pruebas en verde**
   (health y esquema, registro/login/logout/`me`, catálogo y poses, CRUD de gatos,
   límite de tres gatos, validación contra catálogo, matriz RBAC, transiciones de
   estado y la consola de administración). Usan SQLite en memoria porque el usuario de
   desarrollo de MySQL no tiene privilegio `CREATE DATABASE`.
2. **Verificación en vivo contra MySQL** — `python scripts/check_backend.py` con el
   servidor de desarrollo en marcha: **19/19 comprobaciones superadas**. Cubrió el
   flujo completo de cuentas y gatos sobre el motor real y borró sus propios datos al
   terminar (`Limpieza: 7 cuentas, 6 opciones y 6 poses de prueba eliminadas`).

Comandos reproducibles:

```bash
python -m venv .venv && .venv/Scripts/python.exe -m pip install -r backend/requirements.txt
cd backend && python manage.py migrate && python -m pytest
python manage.py runserver 127.0.0.1:8000     # en otra consola
python scripts/check_backend.py               # verificación en vivo + limpieza
```

## Verificación de la consola de administración (2026-11-04)

Ramas: `backend/django-admin`. Nueve entidades registradas en `backend/apps/*/admin.py`
(con `manage.py check`: 0 errores y 0 advertencias).

1. **Pruebas automatizadas** — `python -m pytest tests/test_admin.py` dentro del suite completo:
   las nueve pantallas de listado y de alta se abren; el formulario de gatos rechaza opciones fuera
   del catálogo y las premium sin plan; las acciones de paquetes y trabajos respetan la máquina de
   estados (una transición ilegal deja el estado intacto); `make_failed` registra `ADMIN_MANUAL`;
   publicar cambia la visibilidad; y una pose con stickers no se borra.
2. **Verificación en vivo contra MySQL** — se creó una cuenta de consola temporal y, con el cliente
   de Django sobre la base de desarrollo, se abrieron las 9 listados y los 9 formularios de alta:
   todos devolvieron **200**. Las cuatro consultas de autocompletado (`user`, `pose`, `cat`)
   también respondieron 200; `poses` y `gatos` volvieron 0 opciones porque el catálogo de
   desarrollo sigue vacío (limitación ya registrada).
3. **Limpieza** — la cuenta temporal se eliminó y se borraron las 2 sesiones huérfanas que dejó la
   comprobación. En la base de desarrollo queda únicamente la cuenta previa `alexvb`; no se crearon
   datos de dominio.

Comprobación reproducible (sin credenciales en el repositorio):

```bash
cd backend
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000     # abrir http://127.0.0.1:8000/admin/
python -m pytest tests/test_admin.py
```

## Incidencias y decisiones

- `mysqlclient` no publica ruedas para Python 3.14 y exige compilador en Windows; se
  usa **PyMySQL** con el shim `install_as_MySQLdb()`. No hizo falta corregir la versión
  reportada: PyMySQL 1.2.3 ya informa `version_info = (2, 2, 8)` y pasa el chequeo de
  Django. Registrado en [ADR-005](../decisions/ADR-005-autenticacion-y-rbac.md).
- Las credenciales de desarrollo viven solo en `.env` (ignorado por Git); este informe
  no las reproduce.
- Existe un archivo `backend/.env` vacío heredado de la estructura inicial. La
  configuración carga únicamente la `.env` de la raíz del repositorio; conviene borrarlo
  para no confundir a un integrante nuevo.
- El catálogo queda **sin opciones reales**: `assets/catalog.json` está vacío mientras la
  diseñadora entrega los recursos (P06). El endpoint `/api/catalog/` responde 200 con
  `categories: {}` y las pruebas inyectan sus propias opciones. No debe presentarse como
  catálogo terminado en la demo hasta P08.
- Comprobaciones 1, 2, 5 y 6 continúan abiertas; P02 no puede marcarse como terminada
  hasta que el Integrante A valide Flet y el Integrante C compose el primer gato.

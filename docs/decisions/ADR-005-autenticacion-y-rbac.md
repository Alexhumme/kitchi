# ADR-005 — Autenticación por token, permisos RBAC y motor de datos

- **Estado:** Aceptado
- **Fecha:** 2026-11-04
- **Responsables:** Alex Valdelamar (Integrante B — backend y datos)

## Contexto y problema

El plan maestro dejaba tres decisiones abiertas con fecha límite en la semana 1–2
([01_MASTER_PLAN.md](../01_MASTER_PLAN.md), tabla de decisiones pendientes):

1. El mecanismo de autenticación entre el cliente Flet y Django (P03).
2. El modelo de autorización sobre los recursos del sistema.
3. El motor de base de datos realista para desarrollar sin bloquear el clon limpio (P29).

La API debe poder demostrarse desde Swagger sin depender de la interfaz, el cliente
Flet se ejecuta en un origen distinto (`127.0.0.1:8550`) y la rúbrica exige que el
manejo de errores y los permisos sean visibles y explicables.

## Alternativas evaluadas

**Autenticación**

1. **Sesiones de Django con cookie.** Descartada: el origen de Flet difiere del de la
   API, lo que obliga a configurar cookies entre dominios y CSRF en cada petición; complica
   la prueba desde Swagger y desde la app móvil.
2. **JWT (simplejwt).** Descartada para el MVP: añade expiración, refresh y dos tokens
   que el proyecto no necesita en un entorno local de cuatro semanas.
3. **Token de Django (`rest_framework.authtoken`).** Elegida: un encabezado
   `Authorization: Token <clave>`, una tabla, invalidación trivial en el logout y
   soporte nativo en DRF y en el cliente HTTP de Flet.

**Autorización**

1. **Permisos por modelo de Django (`auth.Permission`).** Descartada como mecanismo
   principal: es granular pero ruidosa para un MVP con seis dominios.
2. **RBAC por rol y por recurso.** Elegida: dos roles (`member`, `admin`) y una matriz
   explícita por recurso (`owned` / `shared`) en
   [`backend/apps/accounts/permissions.py`](../../backend/apps/accounts/permissions.py).
   La propiedad del recurso se comprueba a nivel de objeto, así que un miembro solo
   opera sobre sus propios gatos, paquetes, publicaciones y trabajos.

**Motor de datos**

1. **Solo MySQL 8.** Mantenido como motor de desarrollo y de demostración; ya crea el
   esquema con las migraciones de Django.
2. **Solo SQLite.** Descartado: el plan declara MySQL y el cambio exigiría justificación.
3. **MySQL + fallback SQLite por variable de entorno.** Elegido: `DB_ENGINE=sqlite`
   permite que un clon limpio o un equipo sin MySQL levante la app en minutos. El
   modelo de datos y las migraciones no cambian entre motores.

## Decisión

- La autenticación es por **token de Django**, emitido en `/api/auth/register/` y
  `/api/auth/login/`, invalidado en `/api/auth/logout/`. `SessionAuthentication` queda
  habilitado solo para probar la API desde Swagger en el mismo navegador.
- La autorización es **RBAC con dos roles** (`member`, `admin`) sobre una matriz de
  recursos. Los recursos `owned` exigen propiedad además del rol; los `shared`
  (catálogo y poses) son de lectura autenticada y escritura restringida a `admin`.
  La lectura de un gato ajeno se permite únicamente cuando el gato está publicado.
- El motor de datos es **MySQL 8** (`DB_ENGINE=mysql`, valor por defecto) con
  **fallback a SQLite** (`DB_ENGINE=sqlite`). El driver es **PyMySQL** con el shim
  `install_as_MySQLdb()`, porque `mysqlclient` no publica ruedas para Python 3.14 y
  exigiría un compilador en cada equipo del equipo.
- Las pruebas automatizadas usan SQLite en memoria
  ([`backend/config/settings_test.py`](../../backend/config/settings_test.py)): el
  usuario de desarrollo de MySQL no tiene privilegio `CREATE DATABASE` y no se le
  concede. Las migraciones sí se validan contra MySQL con `manage.py migrate`.

## Justificación

El token resuelve el problema del origen cruzado sin librerías nuevas y hace que la
demo desde Swagger sea directa. La matriz RBAC es una estructura que se puede explicar
en la sustentación en dos minutos y que centraliza la regla «el backend autoriza, la
interfaz no» exigida por [`AGENTS.md`](../../../AGENTS.md). El fallback a SQLite
protege la fecha límite: si un equipo no puede instalar MySQL, el proyecto sigue
arrancando y la entrega no depende de un servidor externo.

## Consecuencias y riesgos

- **Obligatorio:** toda vista nueva declara su recurso en `RESOURCES` o en
  `rbac_resource`; si no, se trata como `shared` y un miembro no podrá escribir en ella.
  Es un fallo ruidoso y preferible al permiso abierto.
- **Obligatorio:** el perfil (`user_profiles`) se crea con la señal `post_save` de
  `User`. Cualquier creación de usuario fuera del ORM (scripts, fixtures) debe asegurar
  el perfil o el rol caerá al valor por defecto `member`.
- **Riesgo:** los tokens no caducan. Aceptable para el prototipo local; se documenta
  como limitación en la guía viva y se mitigaría con expiración si el tiempo lo permite.
- **Riesgo:** PyMySQL no es el driver «oficial» de Django para MySQL. Mitigado: funciona
  con el shim, está fijado en `requirements.txt` y la conexión quedó verificada con
  `migrate` y `/api/health/` (evidencia en [`reports/week1-validation.md`](../reports/week1-validation.md)).
- **Riesgo:** las pruebas no ejercitan el dialecto MySQL. Mitigado: P29 valida el
  esquema aplicado en MySQL desde un clon limpio.
- Las publicaciones y los paquetes conservan la semántica de lectura pública prevista en
  [04_DATA_MODEL.md](../04_DATA_MODEL.md); al implementar P18 deben marcarse con
  `rbac_public = True` en las rutas de lectura.

## Documentos afectados

- [05_API_CONTRACTS.md](../05_API_CONTRACTS.md) — mecanismo de autenticación fijado.
- [04_DATA_MODEL.md](../04_DATA_MODEL.md) — motor de datos y rol/perfil de usuario.
- [03_ARCHITECTURE.md](../03_ARCHITECTURE.md) — estructura real de `backend/apps/`.
- [01_MASTER_PLAN.md](../01_MASTER_PLAN.md) — cierra las decisiones pendientes de autenticación y motor.
- [12_GUIA_PLATAFORMA.md](../12_GUIA_PLATAFORMA.md) — secciones de arquitectura, datos y limitaciones.

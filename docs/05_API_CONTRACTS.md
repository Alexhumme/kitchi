# 05 · Contratos de la API REST — Kitchi Studio

Endpoints, OpenAPI/Swagger, comportamiento de trabajos y gestión de errores · Versión 1.1 · 28 de octubre de 2026

> La API ofrece contratos estables entre Flet y Django. Los endpoints propuestos son conceptuales; **sus nombres definitivos se registran en este documento** antes de desarrollar frontend y backend en paralelo. Modificar un contrato compartido requiere coordinar con los responsables y registrar la decisión en [`decisions/`](decisions/). La documentación navegable es un requisito académico (AR-06 / AC-18).

## Documentación automática

| Método | Endpoint | Propósito | Autenticación |
| --- | --- | --- | --- |
| `GET` | `/api/health/` | Comprobar disponibilidad de la API | Pública |
| `GET` | `/api/schema/` | Esquema OpenAPI 3 | Pública |
| `GET` | `/api/docs/` | Swagger UI navegable | Pública |

Reglas:

- El esquema se genera con **drf-spectacular** y debe incluir los endpoints, parámetros, respuestas y códigos de error.
- Swagger debe permitir probar al menos un endpoint público y uno autenticado.
- El esquema se versiona en `shared/contracts/openapi.yaml` cuando esté estable.
- Si la documentación no carga, la entrega no cumple AC-18.

## Endpoints propuestos

Estado a 4 de noviembre de 2026. **Implementado** significa que el endpoint existe, está
servido por la API y tiene prueba automatizada; no que la interfaz ya lo consuma.

| Método | Endpoint | Propósito | Autenticación | Estado |
| --- | --- | --- | --- | --- |
| `POST` | `/api/auth/register/` | Registrar un usuario | Pública | Implementado y consumido por Flet |
| `POST` | `/api/auth/login/` | Iniciar sesión | Pública | Implementado y consumido por Flet |
| `POST` | `/api/auth/logout/` | Cerrar sesión | Requerida | Implementado y consumido por Flet |
| `GET` | `/api/auth/me/` | Consultar el usuario actual | Requerida | Implementado y consumido por Flet |
| `GET` | `/api/catalog/` | Obtener opciones disponibles | Pública | Implementado, sembrado provisional y consumido por Flet |
| `GET` | `/api/poses/` | Obtener las poses | Pública | Implementado, sembrado provisional y consumido por Flet |
| `GET` | `/api/cats/` | Listar gatos propios | Requerida* | Implementado y consumido por Flet |
| `POST` | `/api/cats/` | Crear un gato | Requerida* | Implementado y consumido por Flet |
| `GET` | `/api/cats/{id}/` | Consultar un gato | Dueño / pública si publicada | Implementado |
| `PATCH` | `/api/cats/{id}/` | Actualizar su configuración | Solo dueño | Implementado y consumido por Flet |
| `DELETE` | `/api/cats/{id}/` | Eliminar un gato propio | Solo dueño | Implementado y consumido por Flet |
| `POST` | `/api/sticker-packs/` | Solicitar generación de un paquete | Requerida* | Pendiente (P15) |
| `GET` | `/api/sticker-packs/{id}/` | Consultar estado y resultado | Dueño | Pendiente (P15) |
| `GET` | `/api/sticker-packs/{id}/download/` | Descargar el paquete completo o un sticker | Dueño | Pendiente (P14/P15) |
| `POST` | `/api/ai-jobs/` | Solicitar una transformación por IA | Requerida | Pendiente (P16) |
| `GET` | `/api/ai-jobs/{id}/` | Consultar el resultado de IA | Dueño | Pendiente (P16) |
| `GET` | `/api/publications/` | Explorar el hub (paginado) | Pública | Pendiente (P18) |
| `POST` | `/api/publications/` | Publicar una creación | Requerida | Pendiente (P18) |
| `GET` | `/api/publications/{id}/` | Ver una publicación | Pública | Pendiente (P18) |
| `PATCH` | `/api/publications/{id}/` | Editar una publicación propia | Solo dueño | Pendiente (P18) |
| `DELETE` | `/api/publications/{id}/` | Retirar una publicación propia | Solo dueño | Pendiente (P18) |
| `POST` | `/api/publications/{id}/copy/` | Copiar una creación pública | Requerida | Pendiente (P19) |

Los modelos de `sticker_packs`, `stickers`, `publications` y `generation_jobs` ya existen
con sus migraciones (P11); lo pendiente en esas filas son los endpoints.

\* El modo invitado funciona con almacenamiento local del navegador; la API autoriza operaciones de cuenta solo para usuarios registrados. La persistencia en servidor de invitados es decisión pendiente ([01_MASTER_PLAN.md](01_MASTER_PLAN.md)).

### Consumo desde Flet (9 de noviembre de 2026)

El cliente [`frontend/src/kitchi/api.py`](../frontend/src/kitchi/api.py) resuelve la URL desde
`KITCHI_API_URL`, `API_BASE_URL` o la `.env` de la raíz. Si no hay URL, queda en modo local
sin llamar a la API. Los endpoints consumidos hoy son `health`, `catalog`, `poses`,
`register`, `login`, `logout`, `me`, `list/create/update/delete` de gatos y
`publications` (este último todavía responde 404 y la interfaz lo muestra como pendiente).

- El cliente envía `Authorization: Token <clave>` y normaliza los errores del envoltorio
  `{error: {code, message, details}}`; `ApiError.user_message()` extrae el primer mensaje de
  campo para mostrarlo en la pantalla.
- `/api/poses/` está paginado: el cliente lee `results`.
- La configuración que envía Flet es la del contrato backend
  (`{"schema_version": 1, "fur": "tabby", ...}`); al leer un gato, `cat_from_api()` aplana
  bloques como `{"fur": {"code": "bicolor"}}` a `"bicolor"`.
- El catálogo del backend es la autoridad de códigos; el frontend adapta su catálogo local y
  conserva descripciones/swatches solo para la previsualización.

## Convenciones

- Formato JSON; fechas en ISO 8601 UTC.
- Listados paginados con `page` y `page_size`; el hub usa paginación por defecto.
- Las rutas de archivos se devuelven como URLs autorizadas, no como rutas absolutas del servidor.
- Los identificadores de recursos se validan contra el catálogo; el cliente no puede enviar nombres de archivo arbitrarios.
- La autenticación es por **token de Django** (`Authorization: Token <clave>`), decisión
  registrada en [ADR-005](decisions/ADR-005-autenticacion-y-rbac.md). `SessionAuthentication`
  queda habilitado solo para probar la API desde Swagger en el mismo navegador.
- La autorización es **RBAC** con dos roles (`member`, `admin`) y política por recurso:
  los recursos propios (`cats`, `sticker_packs`, `publications`, `generation_jobs`) se
  leen y escriben solo por su dueño o por un admin; los compartidos (`catalog`, `poses`)
  son de lectura autenticada y escritura restringida a `admin`.
- CORS se configura solo para los orígenes locales de Flet; no se usa `*` en producción.

## Comportamiento de la generación

La petición de generar un paquete responde con un identificador de trabajo y **no espera** a que terminen los seis stickers.

Respuesta inicial de `POST /api/sticker-packs/`:

```json
{
  "job_id": "identificador",
  "status": "pending"
}
```

- La interfaz consulta el estado mediante `GET /api/sticker-packs/{id}/` (consulta periódica; polling simple es suficiente para el prototipo local).
- Cuando el trabajo finaliza, el backend devuelve las rutas o URL autorizadas para descargar los resultados.
- No es necesario introducir WebSockets para comunicar el progreso.
- Estados posibles del trabajo: `pending` → `running` → `completed` / `failed`. Las transiciones se validan en el backend ([04_DATA_MODEL.md](04_DATA_MODEL.md)).
- Si una pose falla, el paquete no se marca como `completed` hasta validar los seis archivos.

Ejemplo de respuesta completada:

```json
{
  "job_id": "identificador",
  "status": "completed",
  "stickers": [
    {"pose": "greeting", "url": "/media/packs/.../greeting.png"},
    {"pose": "happy", "url": "/media/packs/.../happy.png"}
  ],
  "completed_at": "2026-11-20T15:04:05Z"
}
```

## Gestión de errores

Los errores deben tener respuestas coherentes:

| Código | Significado | Uso en el proyecto |
| --- | --- | --- |
| `400` | Datos inválidos | Configuración fuera de catálogo, archivos rechazados |
| `401` | Usuario no autenticado | Operaciones de cuenta sin sesión |
| `403` | Usuario sin permisos | Invitado que intenta publicar, editar gato ajeno |
| `404` | Recurso inexistente | Gato, paquete o publicación inexistente |
| `409` | Conflicto de estado o límite alcanzado | Superar el límite de tres gatos |
| `413` | Archivo demasiado grande | Fotografía que excede el tamaño permitido |
| `429` | Límite de solicitudes excedido | Control de uso del plan gratuito |
| `500` | Error interno no esperado | Fallo no capturado |

Formato de error propuesto:

```json
{
  "error": {
    "code": "CAT_LIMIT_REACHED",
    "message": "El plan gratuito permite hasta tres gatos guardados.",
    "details": {}
  }
}
```

Reglas:

- La interfaz muestra mensajes comprensibles; el backend registra detalles técnicos **sin exponer secretos al usuario** ni trazas internas.
- La validación y autorización residen en el backend; no confiar en identificadores enviados por el cliente.
- Los errores de IA se muestran como estados comprensibles y no como una inferencia exitosa.
- Swagger debe documentar los códigos de error principales.

Códigos de negocio ya implementados en el backend (envoltorio `{error: {code, message, details}}`
en [`backend/apps/core/exceptions.py`](../backend/apps/core/exceptions.py)):

| `error.code` | HTTP | Cuándo se devuelve |
| --- | --- | --- |
| `INVALID_CREDENTIALS` | 401 | Inicio de sesión con usuario o contraseña incorrectos |
| `INVALID_CONFIGURATION` | 400 | La configuración usa recursos fuera del catálogo o incompletos; `details.campos` indica la clave fallida |
| `UNSUPPORTED_SCHEMA_VERSION` | 400 | El documento de configuración declara una versión de esquema desconocida |
| `CAT_NOT_FOUND` | 404 | No existe el gato solicitado |
| `CAT_LIMIT_REACHED` | 409 | Se intenta guardar un cuarto gato en el plan gratuito; `details.limite` y `details.actuales` acompañan el mensaje |

Cualquier otro fallo usa el código genérico `HTTP_<estado>` con el mismo envoltorio, así la
interfaz siempre puede leer `error.code` y `error.message`.

## Próximos pasos para cerrar contratos (tarea P03)

- [~] Fijar nombres definitivos de endpoints y sustituir esta tabla. **Hecho para las
  rutas de cuentas, catálogo, poses y gatos**; quedan por fijar las de paquetes, IA y
  comunidad cuando se implementen (P15/P16/P18).
- [~] Definir esquemas de request/response por endpoint. Los endpoints implementados
  tienen su esquema generado por drf-spectacular y versionado en
  [`shared/contracts/openapi.yaml`](../shared/contracts/openapi.yaml).
- [~] Acordar el mecanismo de autenticación entre Flet y Django: token de Django +
  RBAC, registrado como [ADR-005](decisions/ADR-005-autenticacion-y-rbac.md). El cliente
  Flet ya lo implementa y lo cubre con pruebas; falta la prueba manual de extremo a
  extremo en navegador (tarea P02, comprobación 2).
- [x] Publicar los contratos compartidos en `shared/contracts/`.
- [x] Verificar que `/api/docs/` muestra todos los endpoints y permite probarlos.
- [ ] Añadir ejemplos de error y de respuestas paginadas al documento de contrato. El
  formato de error ya está implementado (envoltura `{error: {code, message, details}}`
  en [`backend/apps/core/exceptions.py`](../backend/apps/core/exceptions.py)) y la
  paginación es la por defecto de DRF (`page`, `page_size`, 12 elementos).

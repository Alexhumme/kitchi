# 05 · Contratos de la API REST — Kitchi Studio

Endpoints, OpenAPI/Swagger, comportamiento de trabajos y gestión de errores · Versión 1.2 · 23 de noviembre de 2026

> La API ofrece contratos estables entre React y Django. React es la única interfaz activa ([ADR-011](decisions/ADR-011-react-interfaz-definitiva.md)); Flet se retiró y sus reportes se conservan como historial. Los endpoints propuestos son conceptuales; **sus nombres definitivos se registran en este documento** antes de desarrollar frontend y backend en paralelo. Modificar un contrato compartido requiere coordinar con los responsables y registrar la decisión en [`decisions/`](decisions/). La documentación navegable es un requisito académico (AR-08 / AC-18).

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
| `POST` | `/api/auth/register/` | Registrar un usuario | Pública | Implementado y consumido por React |
| `POST` | `/api/auth/login/` | Iniciar sesión | Pública | Implementado y consumido por React |
| `POST` | `/api/auth/logout/` | Cerrar sesión | Requerida | Implementado y consumido por React |
| `GET` | `/api/auth/me/` | Consultar el usuario actual | Requerida | Implementado y consumido por React |
| `GET` | `/api/catalog/` | Obtener opciones disponibles | Pública | Implementado, sembrado con assets reales y consumido por React |
| `GET` | `/api/poses/` | Obtener las poses | Pública | Implementado, sembrado con assets reales y consumido por React |
| `GET` | `/api/cats/` | Listar gatos propios | Requerida* | Implementado y consumido por React |
| `POST` | `/api/cats/` | Crear un gato | Requerida* | Implementado y consumido por React |
| `GET` | `/api/cats/{id}/` | Consultar un gato | Dueño / pública si publicada | Implementado |
| `PATCH` | `/api/cats/{id}/` | Actualizar su configuración | Solo dueño | Implementado y consumido por React |
| `DELETE` | `/api/cats/{id}/` | Eliminar un gato propio | Solo dueño | Implementado y consumido por React |
| `POST` | `/api/sticker-packs/` | Solicitar generación de un paquete | Requerida* | Pendiente (P15) |
| `GET` | `/api/sticker-packs/{id}/` | Consultar estado y resultado | Dueño | Pendiente (P15) |
| `GET` | `/api/sticker-packs/{id}/download/` | Descargar el paquete completo o un sticker | Dueño | Pendiente (P14/P15) |
| `POST` | `/api/ai-jobs/` | Solicitar una transformación por IA | Requerida | Pendiente (P16) |
| `GET` | `/api/ai-jobs/{id}/` | Consultar el resultado de IA | Dueño | Pendiente (P16) |
| `GET` | `/api/publications/` | Explorar el hub (paginado, `q=` por título/descripción/autor; `user=` por autor) | Pública | Implementado (P18) |
| `POST` | `/api/publications/` | Publicar un gato propio (409 `PUBLICATION_ALREADY_EXISTS` si ya está publicado) | Requerida | Implementado (P18) |
| `GET` | `/api/publications/{id}/` | Ver una publicación | Pública | Implementado (P18) |
| `PATCH` | `/api/publications/{id}/` | Editar una publicación propia | Solo dueño | Pendiente (P18) |
| `DELETE` | `/api/publications/{id}/` | Retirar una publicación propia | Solo dueño | Pendiente (P18) |
| `GET` | `/api/profiles/{username}/` | Tarjeta pública: alta, `publication_count`, gatos publicados y sus publicaciones públicas | Pública | Implementado (P18) |
| `POST` | `/api/publications/{id}/copy/` | Copiar una creación pública | Requerida | Pendiente (P19) |

Los modelos de `sticker_packs`, `stickers`, `publications` y `generation_jobs` ya existen
con sus migraciones (P11); lo pendiente en esas filas son los endpoints.

\* El modo invitado funciona con almacenamiento local del navegador; la API autoriza operaciones de cuenta solo para usuarios registrados. La persistencia en servidor de invitados es decisión pendiente ([01_MASTER_PLAN.md](01_MASTER_PLAN.md)).

### Consumo desde React (23 de noviembre de 2026)

El cliente tipado [`frontend-react/src/lib/api.ts`](../frontend-react/src/lib/api.ts) resuelve
la URL desde `VITE_API_URL`; si no se define, usa `http://127.0.0.1:8000`. Los endpoints
consumidos hoy son `health`, `catalog`, `poses`, `register`, `login`, `logout`, `me`,
`list/create/update/delete` de gatos, `publications` (listar con `q=`/`user=`, crear y ver) y
`profiles/<username>/` público.

- `frontend-react/src/state/AppContext.tsx` restaura el token de la sesión y el cliente envía
  `Authorization: Token <clave>` en las operaciones privadas.
- El cliente normaliza el envoltorio `{error: {code, message, details}}` en `ApiError`;
  `userMessage()` prioriza los mensajes de `details.campos` para mostrarlos en la interfaz.
- `/api/poses/` acepta respuesta paginada o arreglo; el cliente lee `results` cuando existe.
  `/api/cats/` también acepta ambas formas. El feed de `/api/publications/` es paginado y
  admite `q=` (título/descripción/autor), `user=`, `page` y `page_size`.
- `frontend-react/src/lib/catalog.ts` normaliza la configuración schema 1, valida los códigos
  del catálogo visual y serializa colores y accesorios antes de guardar. El backend sigue
  siendo la autoridad final de validación.
- El catálogo empaquetado aporta nombres, descripciones y swatches para la previsualización;
  `/api/catalog/` confirma los recursos disponibles. El modo invitado guarda en
  `localStorage` y no llama a operaciones privadas de la API.

### Configuración visual y accesorios (23 de noviembre de 2026)

El esquema sigue siendo `schema_version: 1`; la extensión es aditiva y conserva la
compatibilidad con documentos y clientes legacy ([ADR-010](decisions/ADR-010-configuracion-visual-compatible.md)).
Ejemplo de request para
`POST /api/cats/` o `PATCH /api/cats/{id}/`:

```json
{
  "name": "Michi",
  "configuration": {
    "schema_version": 1,
    "fur": {"code": "bicolor", "base_color": "#FFF0D8", "secondary_color": "#F2A15A"},
    "eyes": {"code": "round_green", "color": "#4DAD72"},
    "hair": {"code": "bob", "color": "#6B4226"},
    "top": {"code": "short_sleeved", "color": "#70D6C1"},
    "bottom": {"code": "sweat_pants", "color": "#7B61FF"},
    "accessories": [
      {"code": "round_glasses", "color": "#FF6B6B"},
      {"code": "bow_tie", "color": "#7B61FF"},
      {"code": "moustache", "color": "#211B26"}
    ]
  }
}
```

- `GET /api/catalog/` agrupa por categoría e incluye `compatibility_group` en cada opción.
  La semilla actual registra 53 códigos, incluidos aliases legacy, con rutas de los SVG reales.
- Las cinco categorías base se normalizan a objetos `{code, ...colores}`. Los colores válidos
  son hexadecimales de 6 u 8 dígitos; el backend rechaza slots no permitidos.
- `accessories` admite cero o varios objetos `{code, color?}`. El color es hexadecimal de 6 u
  8 dígitos y se conserva por separado para cada accesorio. Se rechazan duplicados, dos elementos
  del mismo `compatibility_group`, colores inválidos y campos extra; los errores llegan en
  `details.campos.accessories`.
- Se acepta `accessory` legacy (cadena u objeto) y categorías legacy como cadenas. Si se envían
  ambos campos, `accessory` debe coincidir con el primer elemento de `accessories`; una lista
  vacía no admite el espejo legacy.
- La respuesta canónica incluye `accessories` y, si no está vacía, `accessory: {code}` con el
  primer accesorio. React usa la lista; el espejo se conserva para datos y clientes legacy.

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
- CORS permite los orígenes locales de desarrollo, incluidos Vite `5173` y `4173`; no se usa `*` en producción.

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
| `INVALID_CONFIGURATION` | 400 | La configuración usa recursos fuera del catálogo, colores inválidos, accesorios repetidos o incompatibles; `details.campos` indica la clave fallida |
| `UNSUPPORTED_SCHEMA_VERSION` | 400 | El documento de configuración declara una versión de esquema desconocida |
| `CAT_NOT_FOUND` | 404 | No existe el gato solicitado |
| `CAT_LIMIT_REACHED` | 409 | Se intenta guardar un cuarto gato en el plan gratuito; `details.limite` y `details.actuales` acompañan el mensaje |

Cualquier otro fallo usa el código genérico `HTTP_<estado>` con el mismo envoltorio, así la
interfaz siempre puede leer `error.code` y `error.message`.

## Próximos pasos para cerrar contratos (tarea P03)

- [~] Fijar nombres definitivos de endpoints y sustituir esta tabla. **Hecho para las
  rutas de cuentas, catálogo, poses, gatos y comunidad publicada**; quedan por fijar las de
  paquetes, IA, edición/retiro de publicaciones y copia cuando se implementen
  (P15/P16/P18/P19).
- [~] Definir esquemas de request/response por endpoint. Los endpoints implementados
  tienen su esquema generado por drf-spectacular y versionado en
  [`shared/contracts/openapi.yaml`](../shared/contracts/openapi.yaml).
- [x] Acordar el mecanismo de autenticación entre React y Django: token de Django + RBAC,
  registrado como [ADR-005](decisions/ADR-005-autenticacion-y-rbac.md). El cliente React lo
  implementa, las pruebas automatizadas lo cubren y el recorrido autenticado se verificó
  contra MySQL el 23 de noviembre.
- [x] Publicar los contratos compartidos en `shared/contracts/`.
- [x] Verificar que `/api/docs/` muestra todos los endpoints y permite probarlos.
- [ ] Añadir ejemplos de error y de respuestas paginadas al documento de contrato. El
  formato de error ya está implementado (envoltura `{error: {code, message, details}}`
  en [`backend/apps/core/exceptions.py`](../backend/apps/core/exceptions.py)) y la
  paginación es la por defecto de DRF (`page`, `page_size`, 12 elementos).

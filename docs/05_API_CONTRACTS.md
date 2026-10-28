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

| Método | Endpoint | Propósito | Autenticación |
| --- | --- | --- | --- |
| `POST` | `/api/auth/register/` | Registrar un usuario | Pública |
| `POST` | `/api/auth/login/` | Iniciar sesión | Pública |
| `POST` | `/api/auth/logout/` | Cerrar sesión | Requerida |
| `GET` | `/api/auth/me/` | Consultar el usuario actual | Requerida |
| `GET` | `/api/catalog/` | Obtener opciones disponibles | Pública |
| `GET` | `/api/poses/` | Obtener las poses | Pública |
| `GET` | `/api/cats/` | Listar gatos propios | Requerida* |
| `POST` | `/api/cats/` | Crear un gato | Requerida* |
| `GET` | `/api/cats/{id}/` | Consultar un gato | Dueño / pública si publicada |
| `PATCH` | `/api/cats/{id}/` | Actualizar su configuración | Solo dueño |
| `DELETE` | `/api/cats/{id}/` | Eliminar un gato propio | Solo dueño |
| `POST` | `/api/sticker-packs/` | Solicitar generación de un paquete | Requerida* |
| `GET` | `/api/sticker-packs/{id}/` | Consultar estado y resultado | Dueño |
| `GET` | `/api/sticker-packs/{id}/download/` | Descargar el paquete completo o un sticker | Dueño |
| `POST` | `/api/ai-jobs/` | Solicitar una transformación por IA | Requerida |
| `GET` | `/api/ai-jobs/{id}/` | Consultar el resultado de IA | Dueño |
| `GET` | `/api/publications/` | Explorar el hub (paginado) | Pública |
| `POST` | `/api/publications/` | Publicar una creación | Requerida |
| `GET` | `/api/publications/{id}/` | Ver una publicación | Pública |
| `PATCH` | `/api/publications/{id}/` | Editar una publicación propia | Solo dueño |
| `DELETE` | `/api/publications/{id}/` | Retirar una publicación propia | Solo dueño |
| `POST` | `/api/publications/{id}/copy/` | Copiar una creación pública | Requerida |

\* El modo invitado funciona con almacenamiento local del navegador; la API autoriza operaciones de cuenta solo para usuarios registrados. La persistencia en servidor de invitados es decisión pendiente ([01_MASTER_PLAN.md](01_MASTER_PLAN.md)).

## Convenciones

- Formato JSON; fechas en ISO 8601 UTC.
- Listados paginados con `page` y `page_size`; el hub usa paginación por defecto.
- Las rutas de archivos se devuelven como URLs autorizadas, no como rutas absolutas del servidor.
- Los identificadores de recursos se validan contra el catálogo; el cliente no puede enviar nombres de archivo arbitrarios.
- La autenticación exacta (sesión o token) se decide en la tarea P03 y se registra como ADR. Mientras tanto, los contratos usan “Requerida” sin fijar el mecanismo.
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

## Próximos pasos para cerrar contratos (tarea P03)

- [ ] Fijar nombres definitivos de endpoints y sustituir esta tabla.
- [ ] Definir esquemas de request/response por endpoint (JSON).
- [ ] Acordar el mecanismo de autenticación entre Flet y Django (sesión vs token) y registrarlo como ADR.
- [ ] Publicar los contratos compartidos en `shared/contracts/`.
- [ ] Verificar que `/api/docs/` muestra todos los endpoints y permite probarlos.
- [ ] Añadir ejemplos de error y de respuestas paginadas.

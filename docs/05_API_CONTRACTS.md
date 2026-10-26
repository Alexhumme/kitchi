# 05 · Contratos de la API REST — Kitchi Studio

Endpoints, comportamiento de trabajos y gestión de errores · Versión 1.0

> La API ofrece contratos estables entre Flet y Django. Los endpoints propuestos son conceptuales; **sus nombres definitivos se registran en este documento** antes de desarrollar frontend y backend en paralelo. Modificar un contrato compartido requiere coordinar con los responsables y registrar la decisión en [`decisions/`](decisions/).

## Endpoints propuestos

| Método | Endpoint | Propósito | Autenticación |
| --- | --- | --- | --- |
| `POST` | `/api/auth/register/` | Registrar un usuario | Pública |
| `POST` | `/api/auth/login/` | Iniciar sesión | Pública |
| `POST` | `/api/auth/logout/` | Cerrar sesión | Requerida |
| `GET` | `/api/catalog/` | Obtener opciones disponibles | Pública |
| `GET` | `/api/poses/` | Obtener las poses | Pública |
| `GET` | `/api/cats/` | Listar gatos propios | Requerida* |
| `POST` | `/api/cats/` | Crear un gato | Requerida* |
| `GET` | `/api/cats/{id}/` | Consultar un gato | Dueño / pública si publicada |
| `PATCH` | `/api/cats/{id}/` | Actualizar su configuración | Solo dueño |
| `DELETE` | `/api/cats/{id}/` | Eliminar un gato propio | Solo dueño |
| `POST` | `/api/sticker-packs/` | Solicitar generación de un paquete | Requerida* |
| `GET` | `/api/sticker-packs/{id}/` | Consultar estado y resultado | Dueño |
| `POST` | `/api/ai-jobs/` | Solicitar una transformación por IA | Requerida |
| `GET` | `/api/ai-jobs/{id}/` | Consultar el resultado de IA | Dueño |
| `GET` | `/api/publications/` | Explorar el hub | Pública |
| `POST` | `/api/publications/` | Publicar una creación | Requerida |
| `POST` | `/api/publications/{id}/copy/` | Copiar una creación pública | Requerida |

\* El modo invitado funciona con almacenamiento local del navegador; la API autoriza operaciones de cuenta solo para usuarios registrados. La persistencia en servidor de invitados es decisión pendiente ([01_MASTER_PLAN.md](01_MASTER_PLAN.md)).

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

## Gestión de errores

Las errores deben tener respuestas coherentes:

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

Reglas:

- La interfaz muestra mensajes comprensibles; el backend registra detalles técnicos **sin exponer secretos al usuario** ni trazas internas.
- La validación y autorización residen en el backend; no confiar en identificadores enviados por el cliente.

## Próximos pasos para cerrar contratos (tarea P03)

- [ ] Fijar nombres definitivos de endpoints y sustituir esta tabla.
- [ ] Definir esquemas de request/response por endpoint (JSON).
- [ ] Acordar el mecanismo de autenticación entre Flet y Django (sesión vs token) y registrarlo como ADR.
- [ ] Publicar los contratos compartidos en `shared/contracts/`.

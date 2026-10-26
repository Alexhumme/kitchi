# 04 · Modelo de datos — Kitchi Studio

Esquema MySQL, entidades, relaciones y decisiones de modelado · Versión 1.0

> La base de datos representa usuarios, configuraciones de personajes, paquetes de stickers, publicaciones y trabajos de generación. **No** es necesario crear tablas para cada una de las 729 combinaciones posibles. Los nombres son una propuesta inicial y se normalizan al fijar el esquema definitivo.

## Entidades principales

| Entidad | Propósito | Campos principales |
| --- | --- | --- |
| `users` | Usuarios registrados | `id`, `username`, `email`, `password`, `created_at`, `updated_at` |
| `cats` | Personajes guardados | `id`, `user_id`, `name`, `configuration`, `created_at`, `updated_at` |
| `sticker_packs` | Paquetes de stickers | `id`, `cat_id`, `status`, `created_at`, `completed_at` |
| `stickers` | Imágenes individuales | `id`, `pack_id`, `pose_id`, `file_path`, `status` |
| `poses` | Catálogo de poses | `id`, `code`, `name`, `asset_path`, `is_active` |
| `catalog_options` | Opciones del editor | `id`, `category`, `code`, `asset_path`, `is_premium`, `is_active` |
| `publications` | Creaciones compartidas | `id`, `cat_id`, `user_id`, `title`, `description`, `visibility`, `created_at` |
| `generation_jobs` | Trabajos de IA o composición | `id`, `user_id`, `job_type`, `status`, `created_at`, `started_at`, `completed_at`, `error_code` |

## Relaciones

```
USERS ||──o{ CATS          (creates)
USERS ||──o{ PUBLICATIONS  (publishes)
USERS ||──o{ GENERATION_JOBS (requests)
CATS  ||──o{ STICKER_PACKS (generates)
CATS  ||──o{ PUBLICATIONS  (published_as)
STICKER_PACKS ||──o{ STICKERS (contains)
POSES ||──o{ STICKERS      (appears_in)
```

- Un usuario crea muchos gatos; cada gato pertenece a un usuario.
- Un gato produce muchos paquetes; cada paquete contiene exactamente seis stickers cuando completa.
- Una pose puede aparecer en muchos stickers; el catálogo de poses controla qué poses existen.
- Un gato puede tener cero o una publicación; la publicación conoce al gato y a su autor.
- Un usuario solicita muchos trabajos de generación (IA o composición).

## Decisiones de modelado

### Configuración del gato

Para el MVP se almacena como **JSON validado en una columna de MySQL**. Esto facilita guardar combinaciones de atributos sin crear numerosas tablas. Los recursos válidos siguen definidos por el catálogo.

Estructura conceptual del documento de configuración (las claves definitivas deben coincidir con los recursos que produzca la diseñadora — ver [06_DESIGN_SYSTEM.md](06_DESIGN_SYSTEM.md)):

```json
{
  "schema_version": 1,
  "fur": {
    "pattern": "tabby",
    "base_color": "#F2A15A",
    "secondary_color": "#FFF0D8"
  },
  "eyes": {
    "style": "round",
    "color": "#4DAD72"
  },
  "hair": {
    "style": "short_fringe",
    "color": "#684632"
  },
  "top": "hoodie",
  "bottom": "shorts",
  "accessory": "bow"
}
```

El backend valida los identificadores de recurso contra el catálogo disponible. **No debe aceptar nombres de archivos arbitrarios enviados por el cliente.**

### Archivos

Los PNG y las fotografías no se almacenan como cadenas Base64 en las tablas. La base de datos guarda rutas relativas o identificadores de almacenamiento; los archivos viven en el sistema de archivos local durante la demostración (directorio `storage/`).

### Contraseñas

Se gestionan mediante el sistema de autenticación de Django, que incluye hashing y mecanismos de validación. **Nunca** se almacenan en texto plano.

### Invitados

No necesitan una fila en `users` si sus gatos se almacenan en el navegador y no existe sincronización entre dispositivos. Si más adelante se requiere persistencia en el servidor, se diseña una identidad anónima temporal (decisión pendiente, [01_MASTER_PLAN.md](01_MASTER_PLAN.md)).

### Copias

Copiar una creación pública debe crear un **nuevo gato propiedad del usuario actual**. No debe modificar la creación original ni su configuración.

### Publicaciones

La publicación y el personaje son entidades distintas. El usuario puede dejar de publicar un gato sin que eso obligue a borrar el gato de su colección.

### Estados

Los trabajos deben tener estados definidos: `pending`, `running`, `completed`, `failed`. Las transiciones se validan en el backend.

## Restricciones e índices

Como mínimo:

- Unicidad de `username` y `email`.
- Claves foráneas con políticas explícitas de eliminación.
- Índices para `cats.user_id`, `publications.user_id`, `publications.visibility` y `stickers.pack_id`.
- Validación del límite de gatos mediante una operación transaccional o mecanismo equivalente que evite dos creaciones simultáneas que excedan el límite.
- Acceso a publicaciones públicas sin permitir modificar datos de otros usuarios.
- No confiar en los identificadores enviados por el cliente para autorizar modificaciones.

## Migraciones y configuración

- El esquema se administra mediante **modelos y migraciones de Django**. No crear manualmente las tablas y después intentar sincronizarlas con los modelos.
- La configuración de MySQL utiliza **variables de entorno** (ver [`.env.example`](../.env.example)). Se añade un archivo de ejemplo con nombres de variables, sin credenciales reales.
- Las migraciones y cambios de esquema los aprueba un único responsable de integración ([03_ARCHITECTURE.md](03_ARCHITECTURE.md)).

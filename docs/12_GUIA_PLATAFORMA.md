# 12 · Guía viva de la plataforma — Kitchi Studio

Documento de estudio para la sustentación · Versión 0.4 · 9 de noviembre de 2026

> **Estado:** documento vivo, casi vacío a propósito. Se completará **por incrementos** a medida que la aplicación se implemente. No describe funcionalidades que aún no existen.
>
> **Para quién es:** todos los integrantes del equipo, incluida la diseñadora. Es la lectura previa a la presentación y la base para responder preguntas individuales sobre cualquier parte del proyecto.

## Para qué sirve

- Explicar qué problema resuelve Kitchi Studio y para quién.
- Recorrer el flujo completo de la plataforma sin leer el código.
- Entender cómo se conectan la interfaz, la API, la base de datos y el motor gráfico.
- Preparar una demo de 10 minutos y las preguntas individuales del profesor.
- Dejar por escrito las decisiones y limitaciones que un integrante nuevo necesitaría conocer.

## Regla de actualización

1. Cada incremento que cambie el funcionamiento, una pantalla, la arquitectura, la instalación o la demo debe actualizar este documento en el mismo cambio.
2. Se escribe en lenguaje claro: **qué hace**, **cómo se usa** y **por qué se diseñó así**.
3. No se copia código completo; se explican los módulos y se enlazan los archivos.
4. No se marca como terminado nada que solo exista en el diseño o esté simulado.
5. Al final de cada incremento se añade una fila al registro de la última sección.

## 1. Resumen en una frase

Kitchi Studio es una aplicación web móvil con la que una persona que no sabe dibujar
compone un gato chibi combinando recursos 2D por capas, guarda hasta tres personajes,
pide un paquete de seis stickers PNG transparentes y comparte sus creaciones en un hub.

**Estado a 9 de noviembre:** el backend (API, datos, cuentas, permisos y documentación
OpenAPI) está implementado y en uso. La interfaz Flet Web existe y consume la API para
catálogo, poses, cuentas y gatos; el editor ya permite crear, previsualizar con
placeholders de color, guardar y editar hasta tres gatos. El motor de composición y los
endpoints de stickers, publicaciones e IA siguen pendientes, así que el flujo completo de
usuario todavía no puede recorrerse de principio a fin.

## 2. Problema, usuario y propuesta de valor

- **Problema:** conseguir stickers personalizados exige saber ilustrar o pagar una
  herramienta de diseño.
- **Usuario previsto:** cualquier persona desde el navegador del teléfono; sin cuenta
  compone y guarda en el navegador; con cuenta guarda en la API. Ambas rutas de
  composición y guardado ya existen (P10/P12). Publicar y copiar creaciones sigue
  pendiente del hub (P18/P19).
- **Propuesta de valor:** el motor 2D por capas. En lugar de producir 3⁶ = 729
  ilustraciones, se mantiene un catálogo de 18 opciones conceptuales (3 por cada uno de
  los 6 campos) y la apariencia se reconstruye desde una configuración ([ADR-002](decisions/ADR-002-character-rendering.md)).
- **IA:** diferenciador opcional para transformar una fotografía; el flujo manual no
  depende de ella ([ADR-003](decisions/ADR-003-ai-strategy.md)).

## 3. Flujo completo del usuario

Lo que ya se puede recorrer (9 de noviembre):

1. **Entrar sin cuenta.** La app arranca en modo invitado y guarda los gatos en el
   almacenamiento del navegador (`SharedPreferences`). El límite de tres también se aplica
   localmente.
2. **Crear y personalizar.** En **Crear** se eligen las seis categorías del catálogo. La
   previsualización cambia en tiempo real usando **placeholders de color**, porque los
   assets definitivos no existen (P06).
3. **Guardar, editar y borrar.** El gato se guarda en el navegador o, con sesión, en la API.
   Borrar en modo invitado ofrece **Deshacer**; en cuenta pide confirmación y llama a
   `DELETE /api/cats/{id}/`.
4. **Crear cuenta o iniciar sesión.** **Perfil → Crear cuenta / Iniciar sesión** usa
   `/api/auth/register/` y `/api/auth/login/`, guarda el token y mantiene la sesión. Si
   había gatos de invitado y hay espacio, se migran a la cuenta automáticamente.
5. **Mis gatos.** Con sesión, la lista viene de `/api/cats/`; sin sesión, del navegador.
   El contador muestra `n/3` y el backend valida el límite.
6. **Stickers IA.** La pantalla muestra las seis poses reales de `/api/poses/`, pero el
   botón de generar está deshabilitado: faltan motor, paquetes y descargas (P13–P16).
7. **Explorar.** El hub explica el flujo y muestra si `/api/publications/` todavía responde
   404 (P18). No se simulan publicaciones ni copias.

Pendiente para cerrar el recorrido: generar seis PNG, descargarlos, publicar en el hub y
copiar una creación. Nada de eso se presenta como terminado.

## 4. Pantallas y navegación

La barra inferior mantiene cinco secciones: **Navegar**, **Mis gatos**, **Crear**,
**Stickers IA** y **Perfil**. La cabecera muestra el nombre de la cuenta o “Invitado”.

| Pantalla | Qué hace hoy | Qué falta |
| --- | --- | --- |
| **Navegar** (hub de bienvenida) | Presenta el producto, el flujo de tres pasos y el estado del hub; los botones llevan al editor y a Mis gatos | Publicaciones reales, publicar y copiar (P18/P19) |
| **Mis gatos** | Lista los gatos de la cuenta (API) o del navegador (invitado), con editar y eliminar; aplica el límite de tres | — |
| **Crear** | Editor de seis categorías con tres opciones cada una, previsualización de color en tiempo real, guardado/edición y eliminar | Assets finales (P06) y render con Pillow (P13) |
| **Stickers IA** | Muestra las seis poses reales y explica el flujo; el botón está deshabilitado | Paquetes, polling, descargas, IA (P13–P17) |
| **Perfil** | Identidad, sesión, estado de API/catálogo, datos locales y “Acerca de”; abre login/registro y permite actualizar o cerrar sesión | — |
| **Login / Registro** | Formulario con validación local, errores inline, estado de carga y llamada a la API | Verificación manual en navegador y caso de token expirado |
| **Importación de IA / Revisión** | No existen | P16 |

El detalle de widgets y estilos vive en [`06_DESIGN_SYSTEM.md`](06_DESIGN_SYSTEM.md); la
implementación está en `frontend/src/kitchi/screens/`.

## 5. Arquitectura en cinco minutos

Tres capas, un solo backend y sin infraestructura externa ([ADR-001](decisions/ADR-001-frontend-backend.md)):

```
Flet Web (interfaz)            → implementado; render provisional con placeholders
        │ HTTP/JSON · Authorization: Token <clave>
        ▼
Django REST Framework          → sí existe y está en uso
   ├── apps/accounts  cuentas, perfil con rol, token y permisos RBAC
   ├── apps/catalog   opciones del editor y poses
   ├── apps/cats      personajes guardados y límite del plan
   ├── apps/stickers  paquetes y PNG (modelos y estados; sin endpoint aún)
   ├── apps/community publicaciones del hub (modelos; sin endpoint aún)
   ├── apps/ai_jobs   trabajos de IA y composición (modelos; sin endpoint aún)
   └── apps/core      salud del servicio, errores normalizados y estados compartidos
        │
        ├── MySQL 8 (19 tablas creadas por migraciones de Django)
        ├── storage/  PNG y archivos generados (no se versiona)
        └── motor Pillow + adaptador de IA  (pendiente, P13/P14/P16)
```

Cómo se arranca y cómo se comprueba:

| Acción | Comando | Qué ocurre |
| --- | --- | --- |
| Instalar backend | `pip install -r backend/requirements.txt` | Versiones fijadas; PyMySQL como driver porque `mysqlclient` no tiene ruedas para Python 3.14 |
| Instalar frontend | `pip install -e "frontend[dev]"` | Flet 1.1.2 para web y pytest; requiere Python 3.11+ |
| Crear el esquema | `python manage.py migrate` | Aplica las 6 migraciones de dominio sobre MySQL (o SQLite con `DB_ENGINE=sqlite`) |
| Sembrar catálogo provisional | `python scripts/seed_catalog.py` | 18 opciones y 6 poses con rutas de placeholder; idempotente |
| Levantar la API | `python manage.py runserver` | Sirve `/api/…`, `/api/schema/` y `/api/docs/` |
| Levantar la interfaz | `flet run frontend/src/main.py --web --port 8550` | Flet Web en `http://127.0.0.1:8550/`; lee `API_BASE_URL` del `.env` |
| Crear una cuenta de consola | `python manage.py createsuperuser` | Usuario con `is_staff` para entrar en `/admin/` |
| Consola de administración | `http://127.0.0.1:8000/admin/` | Gestión de cuentas, catálogo, poses, gatos, paquetes, publicaciones y trabajos |
| Pruebas del backend | `python -m pytest` (en `backend/`) | 47 pruebas sobre SQLite en memoria |
| Pruebas del frontend | `python -m pytest -q frontend/tests` | 34 pruebas del cliente HTTP, catálogo, sesión, almacenamiento y modelos |
| Verificación en vivo | `python scripts/check_backend.py` | 19 comprobaciones contra el servidor en marcha y MySQL real; autolimpia sus datos |

Puntos de diseño que conviene saber explicar:

- **El catálogo manda.** `apps/catalog/services.py` valida cada documento de configuración
  contra la tabla `catalog_options`; la interfaz nunca envía rutas de archivo ([04_DATA_MODEL.md](04_DATA_MODEL.md)).
- **Los permisos son por rol y por recurso.** `apps/accounts/permissions.py` define una matriz
  RBAC (`member`/`admin`) y la propiedad del recurso; una vista sin recurso declarado se trata
  como compartido y un miembro no puede escribir en ella ([ADR-005](decisions/ADR-005-autenticacion-y-rbac.md)).
- **Los errores hablan un solo idioma.** Todo fallo sale con el envoltorio
  `{error: {code, message, details}}` (`apps/core/exceptions.py`), con códigos de negocio como
  `CAT_LIMIT_REACHED` o `INVALID_CONFIGURATION`.
- **El límite de tres gatos se aplica en el backend** con `select_for_update` sobre la fila del
  usuario, para que dos peticiones simultáneas no lo excedan.
- **El cliente usa los códigos del backend.** `frontend/src/kitchi/catalog.py` reemplaza las
  opciones locales con las de `/api/catalog/` y adapta la configuración normalizada
  (`{"fur": {"code": "tabby"}}` → `"tabby"`). Si la API no responde, conserva el catálogo
  empaquetado y el modo invitado.
- **La sesión decide dónde viven los gatos.** `frontend/src/kitchi/app.py` carga el token de
  `SharedPreferences`; con token usa `/api/cats/`, sin token usa el almacenamiento local. Al
  iniciar sesión, los gatos de invitado se migran a la cuenta si hay espacio.
- **La previsualización es honesta.** El editor dibuja cada pieza con el color del catálogo y
  la etiqueta “Vista previa con placeholders”; no finge que existen los PNG finales.

### 5.1 La consola de administración (`/admin/`)

Es la pantalla desde la que el equipo administra el contenido; no sustituye a la API, usa las
mismas reglas de negocio. Nueve registros, uno por entidad (`apps/*/admin.py`):

| Qué se gestiona | Cómo está configurado |
| --- | --- |
| Cuentas y perfiles | El perfil RBAC (`role`, `premium`) se edita dentro de la pantalla del usuario, no en otra vista |
| Opciones del catálogo y poses | Filtros por categoría y `z_order`/`is_premium`/`is_active` editables desde el listado; acciones para activar o desactivar en lote |
| Gatos | El formulario valida `configuration` contra `validate_configuration` (la misma función de la API); `schema_version` es de solo lectura y se sincroniza al guardar |
| Paquetes y stickers | El estado del paquete es de solo lectura: solo cambia con las acciones `poner en ejecución`, `marcar completados`, `marcar fallidos` y `volver a la cola` |
| Publicaciones | Filtro por visibilidad y acciones para publicar o retirar del hub |
| Trabajos de generación | Las acciones llaman a `mark_started`/`mark_completed`/`mark_failed` del modelo; `ADMIN_MANUAL` queda registrado como causa del fallo |

Dos decisiones que conviene poder explicar:

- **La validación no se duplica.** `apps/cats/admin.py` importa el servicio del catálogo y
  convierte el `APIError` en `ValidationError` del formulario, así que la consola rechaza exactamente
  lo que rechazaría `/api/cats/`, incluidas las opciones premium sin el plan.
- **Las acciones de estado respetan la máquina de estados.** Aplican `transition_to` entidad por
  entidad; las transiciones ilegales se cuentan y se informan como aviso, nunca se fuerzan escribiendo
  el campo. Por eso `status` y `error_code` son de solo lectura en el formulario.

Una pose con stickers generados no se puede borrar (`PROTECT`): la propia consola muestra el error y
la alternativa es desactivarla.

**Dos puertas distintas.** La consola protege a Django con `is_staff` y la sesión del navegador; la
API protege cada recurso con el rol del perfil (`member`/`admin`) y el token. Una cuenta creada con
`createsuperuser` entra en `/admin/` pero sigue siendo `member` para la API: para que un administrador
de contenido también escriba catálogo por REST hay que poner `role = admin` en su perfil desde la
misma consola.

## 6. Modelo de datos

Ocho entidades, administradas con modelos y migraciones de Django sobre MySQL
([04_DATA_MODEL.md](04_DATA_MODEL.md)). Esquema aplicado y verificado el 4 de noviembre de 2026.

| Tabla | Para qué | Puntos clave |
| --- | --- | --- |
| `auth_user` + `user_profiles` | Cuentas y su rol | El perfil se crea solo (señal `post_save`); guarda `role` (`member`/`admin`) y `premium` (plan simulado) |
| `authtoken_token` | Sesión de API | Token de Django; el logout borra la fila y el siguiente login genera una nueva |
| `catalog_options` | Opciones del editor | Única por `(category, code)`, con `z_order`, `is_premium` e `is_active` |
| `poses` | Catálogo de poses | `code` único; un paquete completo usa las activas |
| `cats` | Personajes guardados | `configuration` es JSON validado; nombre único por usuario; índice `(user, created_at)` |
| `sticker_packs` + `stickers` | Paquetes y sus PNG | Un sticker por `(pack, pose)`; el paquete se completa solo cuando los seis están `completed` |
| `publications` | Hub | Separada del gato: retirar la publicación no borra el personaje; `cat` es uno a uno |
| `generation_jobs` | Trabajos de IA y composición | Estados `pending → running → completed/failed` con transiciones validadas |

Decisiones de modelado que hay que saber defender:

- **La configuración se guarda como JSON, no como tablas por combinación.** Evita las 729 filas
  y deja el control de validez en el catálogo. El campo `schema_version` permite cambiar el
  documento sin migrar datos.
- **Los archivos no van en la base de datos.** `stickers.file_path` guarda una ruta relativa a
  `storage/`; las imágenes viven en el sistema de archivos durante la demo.
- **Los estados son una máquina explícita.** `apps/core/models.py` centraliza
  `ALLOWED_TRANSITIONS`; un intento de salto ilegal (p. ej. `pending → completed`) lanza
  `ValueError` y no llega a guardarse. Un trabajo fallido puede volver a `pending` para reintentar.
- **Eliminar es coherente:** borrar un usuario borra sus gatos y trabajos; borrar un gato borra
  su paquete y su publicación; una pose en uso está protegida (`PROTECT`) para no dejar stickers
  huérfanos.

## 7. Motor de stickers

**Estado:** no implementado (P04/P13/P14). Lo que existe hoy es una previsualización
provisional en el editor: seis capas de color construidas con `Container`/`Stack` de Flet,
actualizadas al cambiar la configuración. Las rutas `assets/placeholders/...` del catálogo
son etiquetas de intención, no archivos de imagen.

Cuando se implemente, el motor deberá componer las capas con Pillow, respetar el orden
`z_order`, exportar seis PNG con transparencia y validar que el paquete tenga los seis
archivos antes de marcarlo como completado (P13–P15). El telefono no descargará rutas
absolutas: la API devolverá URLs autorizadas.

## 8. Integración de IA

_Pendiente (P05/P16). Alternativa elegida, inferencia real, privacidad y contingencia._

## 9. Concurrencia, multiprocesamiento y paralelismo

_Pendiente (P20–P22). Qué se mide, con qué operaciones reales y qué significan los resultados._

## 10. Guion de la demo de 10 minutos

_Pendiente (P28/P37). Debe coincidir con [`11_DEMO_SCRIPT.md`](11_DEMO_SCRIPT.md)._

## 11. Preguntas frecuentes de la sustentación

_Pendiente. Añadir preguntas reales de los ensayos y respuestas breves._

## 12. Limitaciones conocidas y trabajo futuro

Implementado y en uso:

- API REST con cuentas por token, catálogo, poses y CRUD de gatos con límite de tres.
- Interfaz Flet Web con cinco secciones, login/registro, sesión persistida, perfil, modo
  invitado y CRUD de gatos; el catálogo y las poses se leen de la API.
- Editor con seis categorías, tres opciones cada una y previsualización de color en tiempo real.
- Migración automática de gatos de invitado a la cuenta al iniciar sesión, si hay espacio.
- Manejo visible de errores en login/registro, guardado, perfil, hub y Mis gatos.
- Documentación OpenAPI/Swagger servida y versionada en `shared/contracts/openapi.yaml`.
- Esquema de datos completo con migraciones aplicadas sobre MySQL 8.
- Permisos RBAC por rol y por recurso; manejo de errores con formato único.
- Consola `/admin/` con las nueve entidades, validación de catálogo en el formulario de gatos y
  acciones de estado que usan la máquina de estados.
- Pruebas: 47 del backend, 34 del frontend y verificación en vivo contra MySQL.

Pendiente de implementar (existe solo el modelo de datos o ni eso):

- **Assets reales:** `assets/catalog.json` sigue vacío; el catálogo sembrado con
  `scripts/seed_catalog.py` usa rutas `assets/placeholders/...` que no son imágenes. El editor
  muestra placeholders de color (P06/P08).
- **Motor de composición con Pillow:** `stickers` y `poses` tienen tabla, pero no hay código que
  genere PNG (P13/P14). Los endpoints de paquetes y descargas tampoco (P15).
- **IA:** `generation_jobs` está listo para registrar trabajos y estados; el adaptador del
  proveedor no existe y `AI_PROVIDER=none` ([ADR-003](decisions/ADR-003-ai-strategy.md)) (P16).
- **Hub:** la pantalla explica el flujo, pero `/api/publications/` aún no existe; no hay
  publicar ni copiar (P18/P19).
- **Concurrencia y paralelismo:** nada implementado (P20–P22).
- **Prueba manual en navegador:** las pantallas se construyen en pruebas y smoke test, pero
  falta recorrer el flujo completo con backend real y verificar la sesión de extremo a extremo.
- **Tokens que no caducan:** el token de Django no tiene expiración; aceptable para un
  prototipo local y registrado como riesgo en [ADR-005](decisions/ADR-005-autenticacion-y-rbac.md).
- **Suscripciones premium:** el campo `premium` y el flag `is_premium` existen y se validan, pero
  no hay ningún flujo de pago; es un plan simulado, como declara [02_REQUIREMENTS.md](02_REQUIREMENTS.md).
- **`backend/.env` vacío:** archivo heredado de la estructura inicial que conviene borrar; la
  configuración solo carga la `.env` de la raíz.

## 13. Glosario

| Término | Significado en este proyecto |
| --- | --- |
| Configuración | Documento JSON con los seis campos del personaje; se valida contra el catálogo |
| Capa | Recurso gráfico que el motor apila en un `z_order` explícito para reconstruir al gato |
| Opción del catálogo | Variante concreta de una categoría (`fur:tabby`, `top:hoodie`); puede ser premium o estar inactiva |
| Pose | Identificador de la postura del sticker; seis poses activas dan un paquete completo |
| Paquete | Solicitud de generación que contiene seis stickers, uno por pose |
| Trabajo de generación | Registro con estado (`pending`/`running`/`completed`/`failed`) de una composición o de una inferencia de IA |
| Publicación | Creación compartida en el hub; entidad distinta del gato, con visibilidad pública o privada |
| Recurso propio / compartido | En RBAC: `owned` lo opera su dueño, `shared` lo escribe solo el rol `admin` |
| Inferencia | Ejecución real del modelo de IA sobre una fotografía; sustituida por la contingencia manual si falla |
| Benchmark | Medición comparativa entre ejecución secuencial y paralela con su fórmula de aceleración |

## Registro de incrementos

| Fecha | Incremento | Qué se documentó | Autor |
| --- | --- | --- | --- |
| 2026-10-28 | Estructura inicial | Se creó el esqueleto y las reglas de actualización; aún no hay funcionalidades implementadas | Equipo |
| 2026-11-04 | Base del backend (P02, P11, P12, P32, P33) | Arquitectura real con las siete apps, modelo de datos aplicado en MySQL, autenticación por token, permisos RBAC, errores normalizados, Swagger y cómo arrancar y verificar cada pieza; limitaciones del lado frontend, motor e IA | Alex Valdelamar |
| 2026-11-04 | Consola de administración (`/admin/`) | Sección 5.1: las nueve entidades registradas, validación de catálogo compartida con la API, acciones de estado sobre la máquina de estados, protección de las poses en uso y el alta de la cuenta de consola con `createsuperuser` | Alex Valdelamar |
| 2026-11-09 | Interfaz Flet e integración con la API (P02, P08, P10, P12, P36, P39) | Se actualizaron resumen, flujo, pantallas, arquitectura y limitaciones: cinco secciones, login/registro, sesión invitado/cuenta, CRUD de gatos, catálogo sembrado y editor con previsualización de placeholders. Se documentó lo que sigue pendiente (assets, Pillow, hub, IA) y se añadieron los comandos de instalación y prueba del frontend | Martin Solano |

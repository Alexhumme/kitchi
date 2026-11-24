# 12 · Guía viva de la plataforma — Kitchi Studio

Documento de estudio para la sustentación · Versión 0.18 · 23 de noviembre de 2026

> **Estado:** documento vivo. Se completa **por incrementos** a medida que la aplicación se implemente y distingue lo verificado de lo pendiente.
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

**Estado a 23 de noviembre:** el backend (API, datos, cuentas, permisos y documentación
OpenAPI) está implementado y en uso. **La interfaz React es la única interfaz activa** y usa
los SVG reales de cuerpo, cabeza delantera, cabello dividido en delante/atrás, prendas y
accesorios: ofrece sliders de color, un mini slider independiente en cada accesorio
seleccionado, previews reales por opción y varios accesorios sin repetir su tipo. La cabeza
se dibuja después de la prenda superior para que los cuellos queden detrás de la cara.
Guarda y edita hasta tres gatos. Las cinco pantallas se verificaron en un navegador real; el
guardado de un gato invitado sobrevive a una recarga. **El hub está implementado**: feed
público con buscador, tarjetas de publicación con preview, perfil público y publicación de
gatos propios desde **Mis gatos** (P18). Flet se retiró y sus reportes quedan como historial
([ADR-011](decisions/ADR-011-react-interfaz-definitiva.md)). El motor de composición, los
endpoints de stickers, la copia de publicaciones y la integración de IA siguen pendientes,
por lo que el flujo completo todavía no puede recorrerse de principio a fin.

## 2. Problema, usuario y propuesta de valor

- **Problema:** conseguir stickers personalizados exige saber ilustrar o pagar una
  herramienta de diseño.
- **Usuario previsto:** cualquier persona desde el navegador del teléfono; sin cuenta
  compone y guarda en el navegador (`localStorage`); con cuenta guarda en la API. La ruta de
  composición y guardado ya existe (P10/P12).
  Publicar y consultar el feed ya funciona (P18); copiar una creación sigue pendiente (P19).
- **Propuesta de valor:** el motor 2D por capas. En lugar de producir todas las
  combinaciones como imágenes independientes, se reconstruye la apariencia desde una
  configuración validada contra el catálogo ([ADR-002](decisions/ADR-002-character-rendering.md)).
  El catálogo actual tiene 53 códigos, incluidos aliases para clientes antiguos, y seis poses;
  las 18 opciones fueron el inventario conceptual inicial, no el total actual.
- **IA:** diferenciador opcional para transformar una fotografía; el flujo manual no
  depende de ella ([ADR-003](decisions/ADR-003-ai-strategy.md)).

## 3. Flujo completo del usuario

Lo que ya se puede recorrer (23 de noviembre):

1. **Entrar sin cuenta.** La app arranca en modo invitado. React guarda los gatos en
   `localStorage`; el límite de tres también se aplica localmente.
2. **Crear y personalizar.** En **Crear** se eligen pelaje, ojos, cabello, parte superior,
   parte inferior y accesorios. Se usan SVG reales: cabello trasero y delantero, cabeza
   delantera sobre la prenda superior, sliders de color, mini slider en cada accesorio
   seleccionado, preview real en cada opción y varios accesorios sin repetir grupo.
3. **Guardar, editar y borrar.** La configuración se valida en el backend antes de
   guardarla. React usa `localStorage` sin sesión y `/api/cats/` con sesión. Borrar en modo
   invitado ofrece **Deshacer**; en cuenta pide confirmación y llama a `DELETE /api/cats/{id}/`.
4. **Crear cuenta o iniciar sesión.** **Perfil → Crear cuenta / Iniciar sesión** usa
   `/api/auth/register/` y `/api/auth/login/`, guarda el token y mantiene la sesión. Si
   había gatos de invitado y hay espacio, se migran a la cuenta automáticamente.
5. **Mis gatos.** Con sesión, la lista viene de `/api/cats/`; sin sesión, del navegador.
   El contador muestra `n/3` y el backend valida el límite.
6. **Stickers IA.** La pantalla muestra las seis poses reales de `/api/poses/`, pero el
   botón de generar está deshabilitado: faltan motor, paquetes y descargas (P13–P16).
7. **Explorar.** El hub muestra las publicaciones públicas con buscador (título,
   descripción y autor con `q=`). Cada tarjeta muestra el preview del gato, el título y
   el autor; tocar el autor abre su perfil público con sus gatos y publicaciones.
8. **Publicar.** Desde **Mis gatos**, la acción de compartir abre un diálogo (título,
   descripción y visibilidad) y el gato queda marcado como "Publicado". Se crea con
   `POST /api/publications/`; publicar dos veces el mismo gato responde 409.

Pendiente para cerrar el recorrido: generar y descargar seis PNG, copiar una creación y
completar la integración de IA. La publicación en el hub ya no está pendiente.

## 4. Pantallas y navegación

La barra inferior mantiene cinco secciones (**Navegar**, **Mis gatos**, **Crear**,
**Stickers IA** y **Perfil**). El engranaje de la cabecera abre **Configuración**
(acerca de la app, efectos, estado de la API y datos locales). La cabecera muestra el
nombre de la cuenta o “Invitado”; el estilo visual es juguetón (bordes gruesos, sombras
sólidas sin desenfoque, rebotes) y los toques vibran en móvil.

| Pantalla | Qué hace hoy | Qué falta |
| --- | --- | --- |
| **Navegar** | Feed público con **buscador** (q por título, descripción y autor) y tarjetas de publicación (preview del gato, título y fila de autor). Tocar el autor abre su **perfil público** | Retirar/editar una publicación (P19 o posterior) |
| **Mis gatos** | Lista los gatos de la cuenta (API) o del navegador (invitado), con editar, publicar y eliminar; aplica el límite de tres | — |
| **Crear** | SVG reales por capas, cabeza delantera sobre la prenda superior, sliders de cabello/prendas/accesorios, previews reales y multiaccesorio por grupo; guardado/edición y eliminar | Motor Pillow y exportación PNG (P13); inventario gráfico final (P06) |
| **Stickers IA** | Muestra las seis poses reales y explica el flujo; el botón está deshabilitado | Paquetes, polling, descargas, IA (P13–P17) |
| **Perfil** | Identidad y cuenta: registro, inicio/cierre de sesión, migración de gatos de invitado, contador n/3 | — |
| **Configuración** (engranaje) | Acerca de la app, efectos, estado de la API y datos locales. React reproduce sonido con Web Audio y vibración | — |
| **Perfil público** | Tarjeta de un usuario: miembro desde, gatos publicados y sus publicaciones | — |
| **Login / Registro** | Formulario con validación local, errores inline, estado de carga y llamada a la API | Caso de token expirado |
| **Importación de IA / Revisión** | No existen | P16 |

El detalle de widgets y estilos vive en [`06_DESIGN_SYSTEM.md`](06_DESIGN_SYSTEM.md); la
implementación está en `frontend-react/src/screens/`.

## 5. Arquitectura en cinco minutos

Tres capas, un solo backend y sin infraestructura externa ([ADR-001](decisions/ADR-001-frontend-backend.md)):

```
React 19 + Vite (interfaz web)      → implementado; editor con SVG reales
        │ HTTP/JSON · Authorization: Token <clave>
        ▼
Django REST Framework          → sí existe y está en uso
   ├── apps/accounts  cuentas, perfil con rol, token y permisos RBAC
   ├── apps/catalog   opciones del editor, grupos de accesorio y poses
   ├── apps/cats      personajes guardados y límite del plan
   ├── apps/stickers  paquetes y PNG (modelos y estados; sin endpoint aún)
   ├── apps/community publicaciones del hub (P18: listar, publicar y perfil público)
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
| Instalar frontend | `cd frontend-react && npm install` | React, TypeScript, Vite y dependencias fijadas en el lockfile |
| Crear el esquema | `python backend/manage.py migrate` | Aplica las migraciones de dominio sobre MySQL (o SQLite con `DB_ENGINE=sqlite`); la extensión de accesorios es no destructiva |
| Sembrar catálogo real | `python scripts/seed_catalog.py` | 53 códigos, incluidos aliases legacy, y seis poses con rutas de SVG reales; idempotente |
| Levantar la API | `python backend/manage.py runserver` | Sirve `/api/…`, `/api/schema/` y `/api/docs/` |
| Levantar React | `cd frontend-react && npm run dev` | Interfaz en `http://127.0.0.1:5173/`; el backend permite ese origen por defecto |
| Crear una cuenta de consola | `python backend/manage.py createsuperuser` | Usuario con `is_staff` para entrar en `/admin/` |
| Consola de administración | `http://127.0.0.1:8000/admin/` | Gestión de cuentas, catálogo, poses, gatos, paquetes, publicaciones y trabajos |
| Pruebas del backend | `python -m pytest -q` (en `backend/`) | 66 pruebas sobre SQLite en memoria |
| Pruebas de React | `cd frontend-react && npm run build && npm run lint` | TypeScript estricto, build de producción y 0 errores de lint; 2 avisos conocidos |
| Compilación de React | `cd frontend-react && npm run build` | TypeScript estricto y bundle de producción con Vite |
| Verificación en vivo | `python scripts/check_backend.py` | 19 comprobaciones contra el servidor en marcha y MySQL real; autolimpia sus datos |

Puntos de diseño que conviene saber explicar:

- **El catálogo manda.** `apps/catalog/services.py` valida cada documento de configuración
  contra la tabla `catalog_options`: existencia, estado activo, plan premium, colores y
  grupos de accesorios. La interfaz nunca envía rutas de archivo
  ([04_DATA_MODEL.md](04_DATA_MODEL.md)).
- **La extensión visual es aditiva.** El esquema sigue siendo `schema_version: 1`.
  `top` y `bottom` admiten color; cada elemento de `accessories` admite su propio `color`
  opcional y permite combinar varios recursos; `accessory` conserva el código del primero
  como espejo para documentos y clientes antiguos. La migración añade
  `catalog_options.compatibility_group` sin alterar datos existentes
  ([ADR-010](decisions/ADR-010-configuracion-visual-compatible.md)).
- **Los permisos son por rol y por recurso.** `apps/accounts/permissions.py` define una matriz
  RBAC (`member`/`admin`) y la propiedad del recurso; una vista sin recurso declarado se trata
  como compartido y un miembro no puede escribir en ella ([ADR-005](decisions/ADR-005-autenticacion-y-rbac.md)).
- **Los errores hablan un solo idioma.** Todo fallo sale con el envoltorio
  `{error: {code, message, details}}` (`apps/core/exceptions.py`), con códigos de negocio como
  `CAT_LIMIT_REACHED` o `INVALID_CONFIGURATION`.
- **El límite de tres gatos se aplica en el backend** con `select_for_update` sobre la fila del
  usuario, para que dos peticiones simultáneas no lo excedan. **El rol `admin` no tiene tope**
  (ADR-005 aplicado a planes): `create_cat` omite el tope cuando el rol del usuario es `admin`.
- **El cliente usa los códigos del backend.** `frontend-react/src/lib/catalog.ts` combina el
  catálogo empaquetado con `/api/catalog/`, normaliza la configuración y conserva el modo
  invitado si la API no responde. `src/lib/characters.ts` relaciona cada código visual con
  su SVG y adapta nombres antiguos sin enviar rutas arbitrarias al backend.
- **La sesión decide dónde viven los gatos.** `frontend-react/src/state/AppContext.tsx`
  restaura la sesión y los datos antes de pintar las pantallas. Sin token usa
  `localStorage`; con token usa `/api/cats/`. Al iniciar sesión, los gatos de invitado se
  migran a la cuenta si hay espacio. La persistencia invitada depende de que el navegador
  permita `localStorage`; no hay un respaldo garantizado en memoria. El manejo visible de un
  almacenamiento bloqueado queda pendiente en P39 y no se presenta como persistencia exitosa.
- **Cada previsualización es honesta.** React apila los SVG reales y usa el mismo
  renderizador para el lienzo y los previews. La previsualización no genera archivos ni
  sustituye los seis PNG finales.
- **El estilo apunta a Wonder.** La firma visual del producto son: bordes asimétricos
  (0 arriba y a la izquierda, canto grueso abajo y a la derecha), sombras duras sin
  desenfoque y rebote elástico al tocar. Los estilos viven en
  `frontend-react/src/styles/`; React reproduce sonido con Web Audio y usa
  `navigator.vibrate` en dispositivos compatibles.

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
| `catalog_options` | Opciones del editor | Única por `(category, code)`, con `z_order`, `is_premium`, `is_active` y `compatibility_group` para accesorios excluyentes |
| `poses` | Catálogo de poses | `code` único; un paquete completo usa las activas |
| `cats` | Personajes guardados | `configuration` es JSON validado; nombre único por usuario; índice `(user, created_at)` |
| `sticker_packs` + `stickers` | Paquetes y sus PNG | Un sticker por `(pack, pose)`; el paquete se completa solo cuando los seis están `completed` |
| `publications` | Hub | Separada del gato: retirar la publicación no borra el personaje; `cat` es uno a uno |
| `generation_jobs` | Trabajos de IA y composición | Estados `pending → running → completed/failed` con transiciones validadas |

Decisiones de modelado que hay que saber defender:

- **La configuración se guarda como JSON, no como tablas por combinación.** Evita
  multiplicar filas por cada variante y deja el control de validez en el catálogo. Las
  cinco categorías base guardan `{code, ...colores}` y `accessories` guarda una lista de
  `{code, color?}` con colores independientes. El backend normaliza los documentos antiguos
  y devuelve `accessory: {code}` con el primer elemento por compatibilidad de datos.
- **El orden de accesorios no es arbitrario.** Si dos opciones comparten
  `compatibility_group` (por ejemplo, dos coronas), el backend rechaza la combinación y
  React sustituye la anterior. Códigos repetidos también se rechazan.
- **Los archivos no van en la base de datos.** `stickers.file_path` guarda una ruta relativa a
  `storage/`; las imágenes viven en el sistema de archivos durante la demo.
- **Los estados son una máquina explícita.** `apps/core/models.py` centraliza
  `ALLOWED_TRANSITIONS`; un intento de salto ilegal (p. ej. `pending → completed`) lanza
  `ValueError` y no llega a guardarse. Un trabajo fallido puede volver a `pending` para reintentar.
- **Eliminar es coherente:** borrar un usuario borra sus gatos y trabajos; borrar un gato borra
  su paquete y su publicación; una pose en uso está protegida (`PROTECT`) para no dejar stickers
  huérfanos.

## 7. Motor de stickers

**Estado:** el motor de exportación no está implementado (P04/P13/P14). React ya ofrece
una previsualización real con SVG: apila cabello trasero, cuerpo completo, prenda inferior,
prenda superior, cabeza delantera, cabello delantero y accesorios, aplicando anclas y
colores en el navegador. La cabeza va después de la prenda superior para que cuellos y
solapas queden detrás de la cara; el cuerpo completo permanece como base posterior para
conservar la alineación. Esta previsualización no genera archivos ni sustituye el paquete
de seis PNG.

Cuando se implemente, el motor deberá componer las capas con Pillow, respetar el orden
`z_order`, exportar seis PNG con transparencia y validar que el paquete tenga los seis
archivos antes de marcarlo como completado (P13–P15). El teléfono no descargará rutas
absolutas: la API devolverá URLs autorizadas. La evidencia del editor SVG está en
[`docs/reports/editor-visual-assets.md`](reports/editor-visual-assets.md).

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

- API REST con cuentas por token, catálogo, poses y CRUD de gatos con límite de tres (sin tope para el rol `admin`).
- Hub: publicación autenticada desde **Mis gatos**, feed público paginado con buscador
  (`q=` por título, descripción y autor), perfil público de usuario con sus gatos y
  publicaciones, y “Gato publicado” como estado en Mis gatos.
- Interfaz React Web como única interfaz activa: cinco secciones (estilo juguetón:
  bordes gruesos, sombras sólidas, rebotes), login/registro, sesión persistida, perfil,
  modo invitado y CRUD de gatos.
- Editor React con SVG reales por capas, cabeza delantera sobre la prenda superior,
  cabello delantero/trasero, sliders de color, previews reales por opción y combinaciones
  multiaccesorio con exclusión por tipo.
- Engranaje de configuración en la cabecera: acerca de la app, efectos, estado de la API
  y vaciado de datos locales. React usa Web Audio y vibración.
- Migración automática de gatos de invitado a la cuenta al iniciar sesión, si hay espacio.
- Recorrido en navegador real de las cinco secciones; creación, guardado, recarga y
  eliminación de un gato invitado. El editor visual también se verificó con interacciones
  reales y persistencia autenticada contra MySQL el 23 de noviembre.
- Manejo visible de errores en login/registro, guardado, perfil, hub y Mis gatos.
- Documentación OpenAPI/Swagger servida y versionada en `shared/contracts/openapi.yaml`.
- Esquema de datos completo con migraciones aplicadas sobre MySQL 8.
- Permisos RBAC por rol y por recurso; manejo de errores con formato único.
- Consola `/admin/` con las nueve entidades, validación de catálogo en el formulario de
  gatos y acciones de estado que usan la máquina de estados.
- Pruebas: 66 del backend, build y lint de React; verificación en vivo contra MySQL y
  evidencia en `docs/reports/editor-visual-assets.md`. Las 46 pruebas Flet son históricas
  y no forman parte de la suite vigente.

Pendiente de implementar y limitaciones conocidas:

- **Inventario gráfico final:** los SVG ya se usan en React y la semilla apunta a rutas
  reales, pero `assets/catalog.json` sigue pendiente como inventario de autoría, licencia
  y aprobación (P06/P08). No se implementan texturas de pelaje hasta su entrega.
- **Motor de composición con Pillow:** `stickers` y `poses` tienen tabla, pero no hay código
  que genere PNG (P13/P14). Los endpoints de paquetes y descargas tampoco (P15).
- **IA:** `generation_jobs` está listo para registrar trabajos y estados; el adaptador del
  proveedor no existe y `AI_PROVIDER=none` ([ADR-003](decisions/ADR-003-ai-strategy.md)) (P16).
- **Hub:** `/api/publications/` permite feed público, búsqueda, creación, detalle y perfil
  público. Falta **copiar una publicación pública** (P19) y la moderación de retiros desde
  la interfaz (solo `/admin/` hoy).
- **Concurrencia y paralelismo:** nada implementado (P20–P22).
- **Prueba manual con cuenta:** el recorrido autenticado creación → publicación → feed se
  verificó el 16 de noviembre; el guardado y la edición visual multiaccesorio contra MySQL
  se verificaron el 23 de noviembre. Falta el caso de token expirado en vivo.
- **Tokens que no caducan:** el token de Django no tiene expiración; aceptable para un
  prototipo local y registrado como riesgo en [ADR-005](decisions/ADR-005-autenticacion-y-rbac.md).
- **Suscripciones premium:** el campo `premium` y el flag `is_premium` existen y se validan, pero
  no hay ningún flujo de pago; es un plan simulado, como declara [02_REQUIREMENTS.md](02_REQUIREMENTS.md).
- **`backend/.env` vacío:** archivo heredado de la estructura inicial que conviene borrar; la
  configuración solo carga la `.env` de la raíz.

## 13. Glosario

| Término | Significado en este proyecto |
| --- | --- |
| Configuración | Documento JSON con cinco categorías base y una lista de accesorios; se valida contra el catálogo |
| Grupo de compatibilidad | Tipo de accesorio que no puede repetirse en un gato; permite combinar, por ejemplo, gafas, corbata y bigote, pero no dos coronas |
| Capa | Recurso gráfico que el motor apila en un `z_order` explícito para reconstruir al gato |
| Opción del catálogo | Variante concreta de una categoría (`fur:tabby`, `top:hoodie`); puede ser premium o estar inactiva |
| Pose | Identificador de la postura del sticker; seis poses activas dan un paquete completo |
| Paquete | Solicitud de generación que contiene seis stickers, uno por pose |
| Trabajo de generación | Registro con estado (`pending`/`running`/`completed`/`failed`) de una composición o de una inferencia de IA |
| Publicación | Creación compartida en el hub; entidad distinta del gato, con visibilidad pública o privada |
| Recurso propio / compartido | En RBAC: `owned` lo opera su dueño, `shared` lo escribe solo el rol `admin` |
| Inferencia | Ejecución real del modelo de IA sobre una fotografía; sustituida por la contingencia manual si falla |
| Benchmark | Medición comparativa entre ejecución secuencial y paralela con su fórmula de aceleración |

## 14. Interfaz React (interfaz definitiva)

Desde el 23 de noviembre de 2026, [`frontend-react/`](../frontend-react/) es la única
interfaz activa: **Vite + React 19 + TypeScript estricto**, con un sistema de diseño propio
en CSS atomizado (`src/styles/`: globals, layout, components/, screens/), `framer-motion`
para resortes y transiciones de pantalla, `lucide-react` para iconos de trazo redondo,
`react-router-dom` para las rutas y la misma API DRF de siempre. La decisión está registrada
en [ADR-011](decisions/ADR-011-react-interfaz-definitiva.md), que sustituye ADR-009.

La implementación Flet y sus pruebas se retiraron del árbol de entrega. Sus ADR y reportes
se conservan como historial: explican por qué se descartó esa interfaz, no una segunda
aplicación que siga funcionando. El campo legacy `accessory: {code}` permanece en el
contrato de datos para no romper documentos guardados.

**Qué ofrece:**

- El gato se dibuja como **SVG completo con los assets reales** (cabello trasero y
  delantero, cuerpo completo, cabeza delantera, prendas y accesorios), no con placeholders
  por contenedores. Los mismos códigos de catálogo producen la figura.
- El selector de opciones muestra previews SVG reales y el lienzo utiliza el mismo
  componente, de modo que la miniatura y la edición no pueden divergir.
- Cabello y prendas tienen slider de color. Cada accesorio seleccionado muestra un mini
  slider propio en el borde inferior de su tarjeta, sin anidarlo dentro del botón; su color
  es independiente y persiste. Varios accesorios pueden convivir y elegir uno del mismo tipo
  sustituye al anterior. “Ninguno” vacía la selección y “Deshacer” restaura el cambio.
- El sonido es real (Web Audio) y la vibración usa `navigator.vibrate`.
- Las animaciones usan resortes (píldora amarilla del tab activo, transiciones entre
  secciones, aparición escalonada de tarjetas del feed).

### Cómo funciona el editor visual

- `src/lib/characters.ts` relaciona cada código con su SVG, caja de coordenadas, ancla,
  orden y grupo de compatibilidad. También normaliza nombres antiguos de recursos.
- `src/components/CatSVG.tsx` importa los SVG como texto, convierte las clases de
  Illustrator en rellenos y apila las capas. Solo tiñe los rellenos base: conserva los
  blancos de detalle, mantiene el lienzo transparente y no añade rectángulos de fondo.
- `src/screens/EditorScreen.tsx` gestiona selección, historial para deshacer, sliders y
  multiaccesorio. Las tarjetas de accesorios separan el botón de selección del mini slider
  para que arrastrar el color no cambie la selección. Cada preview se pasa a `CatSVG`,
  exactamente igual que el lienzo principal.
- `src/lib/catalog.ts` normaliza configuraciones nuevas y antiguas, valida contra el
  catálogo visual y serializa el payload. `src/state/AppContext.tsx` vuelve a normalizar
  y validar antes de persistir en `localStorage` o en la API.
- El orden es cabello trasero → cuerpo completo → inferior → superior → cabeza delantera →
  cabello delantero → accesorios. La cabeza cubre el cuello de la prenda superior sin
  alterar el SVG del cuerpo. Las texturas de pelaje no están implementadas ni se simulan.

**Cómo arrancarla:**

```bash
cd frontend-react && npm install && npm run dev   # http://127.0.0.1:5173
```

El backend debe permitir el origen de Vite: `CORS_ALLOWED_ORIGINS` incluye 5173/4173 por
defecto, pero una variable de entorno con ese nombre **sobrescribe** el valor por defecto;
en ese caso hay que añadir también los orígenes de Vite. El puerto 4173 corresponde a
`npm run preview` (build de producción).

**Estado honesto:** paridad funcional completa (Navegar, Crear, Mis gatos, Stickers IA,
Perfil, Configuración, auth, perfil público), verificada extremo a extremo contra el backend
local (registro → crear → guardar → publicar → aparece en el feed). El editor visual se
verificó además con sliders, mini sliders de accesorios, previews, cabello dividido,
multiaccesorio, deshacer, aleatorio, persistencia de invitado y creación/edición/eliminación
contra MySQL el 23 de noviembre. La cabeza delantera se comprobó en el lienzo y en los seis
previews; el encuadre conserva pies y cabello sin recortarlos. `npm run build` pasa,
`npm run lint` mantiene dos avisos `set-state-in-effect` aceptados y la suite vigente tiene
66 pruebas backend. Quedan pendientes los motores Pillow, seis stickers e IA: la pantalla
Stickers IA declara P13–P16 sin simular resultados.

**Cuándo leerla:** si el profesor pregunta por las alternativas de interfaz, por qué se
retiró Flet o cómo se compone el personaje. La evidencia está en
[`docs/reports/frontend-react.md`](reports/frontend-react.md) y
[`docs/reports/editor-visual-assets.md`](reports/editor-visual-assets.md).

## Registro de incrementos

| Fecha | Incremento | Qué se documentó | Autor |
| --- | --- | --- | --- |
| 2026-10-28 | Estructura inicial | Se creó el esqueleto y las reglas de actualización; aún no hay funcionalidades implementadas | Equipo |
| 2026-11-04 | Base del backend (P02, P11, P12, P32, P33) | Arquitectura real con las siete apps, modelo de datos aplicado en MySQL, autenticación por token, permisos RBAC, errores normalizados, Swagger y cómo arrancar y verificar cada pieza; limitaciones del lado frontend, motor e IA | Alex Valdelamar |
| 2026-11-04 | Consola de administración (`/admin/`) | Sección 5.1: las nueve entidades registradas, validación de catálogo compartida con la API, acciones de estado sobre la máquina de estados, protección de las poses en uso y el alta de la cuenta de consola con `createsuperuser` | Alex Valdelamar |
| 2026-11-09 | Interfaz Flet e integración con la API (P02, P08, P10, P12, P36, P39) | Se actualizaron resumen, flujo, pantallas, arquitectura y limitaciones: cinco secciones, login/registro, sesión invitado/cuenta, CRUD de gatos, catálogo sembrado y editor con previsualización de placeholders. Se documentó lo que sigue pendiente (assets, Pillow, hub, IA) y se añadieron los comandos de instalación y prueba del frontend | Martin Solano |
| 2026-11-10 | Arranque estable del frontend y recorrido verificado (P10, P12, P36, P39) | Nuevo ADR-006 (iconos `ft.Icons`, `Row(wrap=True)` roto en el cliente web 1.1.2, `SharedPreferences` al arrancar); la guía explica el nuevo orden de arranque (armazón → almacenamiento), los iconos y el sustituto `c.flow()`; se actualizó el estado, las pruebas (34 → 42) y la prueba manual en navegador; evidencia en `docs/reports/frontend-flet-web-startup.md` | Alex Valdelamar |
| 2026-11-16 | Hub de publicaciones (P18) | Nuevo ADR-007; feed público con buscador, tarjetas con preview (cuadrícula de 2 columnas), publicación autenticada desde Mis gatos; `/api/publications/` + `/api/profiles/{username}/`; nuevo estilo juguetón global (bordes gruesos, sombras sólidas, rebotes); sonido pendiente de Flet 1.2; evidencia en `docs/reports/p18-hub-publicaciones.md` | Alex Valdelamar |
| 2026-11-16 | Rediseño juguetón | Nuevo ADR-008; bevel asimétrico (libre arriba-izquierda, grueso abajo-derecha), barra de app dorada con separador zig-zag, NavigationBar oscura con indicador amarillo, patrones propios (dots/tiles vía Pillow), botones de plástico sobre `FilledButton`/`OutlinedButton` nativos; sonido pendiente de Flet 1.2 | Alex Valdelamar |
| 2026-11-17 | CSS atomizado sin Tailwind | Se eliminó Tailwind v4 (mezclaba mal con las clases propias bevel); `src/index.css` dividido en `src/styles/` (globals, layout, components/, screens/); cada pantalla y componente tiene sus clases semánticas; misma apariencia 1:1 (verificada en capturas) | Alex Valdelamar |
| 2026-11-17 | Admin sin límite de gatos (RBAC) | El rol `admin` (ADR-005) ya no se ve afectado por el límite del plan gratuito: `create_cat` omite el tope de 3 para admins (backend). El perfil muestra "Plan Admin · Cuenta administrativa · sin límites" con chip Admin y "Espacios ilimitados"; barrera y tope solo para miembro/invitado. Verificado por test backend (admin crea 5 gatos) y por CDP con cuenta admin de prueba (creados 4 gatos por la UI superando 3/3) | Alex Valdelamar |
| 2026-11-17 | Rediseño brutalista de Perfil público, Settings y Acceso | Perfil público: credencial con métricas reales (Gatos, Publicados, Días aquí) sin exponer email y sin rol inventado; tarjetas con borde 2.5px ink y sombra dura; cotización de gatos y de publicaciones en formato PostCard. Settings: cabecera con chevron plano y chip de versión lila; secciones con borde ink y sombra dura; chips de tecnología coloreados por stack (React/Django/MySQL/Fredoka); toggles con iconos en cajas de color. Acceso: sol miel detrás del gato coral, chip KITCHI.STUDIO con pata, campos con borde ink y anillo miel al enfocar, CTA coral con flecha y "Seguir como invitado" como botón blanco brutalista | Alex Valdelamar |
| 2026-11-17 | Perfil como credencial | La vista de Perfil sigue testui/miperfil.html: credencial con avatar, rol (Member/Admin/Invitado), email y alta en kitchi; mini métricas reales (Gatos, Publicados, Días aquí); tarjeta Plan gratuito con barra de capacidad y badge Límite alcanzado al 3/3 (o Pronto para el CTA de ilimitados — nada se simula); accesos Perfil público y Configuración como tiles; para invitados: CTA "Crear cuenta para sincronizar" y Perfil público bloqueado; para cuenta: Cerrar sesión seguro | Alex Valdelamar |
| 2026-11-17 | Explorar como río de publicaciones | El feed sigue testui/feed.html: cabecera con autor, hora relativa ("Hace 37 min") y badge de tipo, escenario grande tintado rotando, título + descripción, pie con pelaje y CTA "Ver gato" al perfil público; buscador pulido; chips (Todo/Gatos funcionando; Packs/Stickers/Creadores deshabilitados como "Pronto", no simulados); el diseño vale también para el perfil público. Nick: like/follows/packs ausentes en el backend — se ocultan en lugar de simularse | Alex Valdelamar |
| 2026-11-17 | Mis gatos coleccionable | La vista de Mis gatos sigue testui/misgatos.html: título con contador, toggle cuadrícula/lista, filtros Todos/Publicados/Borradores, tarjetas con estadio de color, badge Público/Borrador, menú "⋯" (Editar/Publicar/Eliminar), hueco punteado "Crear otro gato" | Alex Valdelamar |
| 2026-11-16 | Interfaz React en paralelo (prototipo de viabilidad) | Nuevo ADR-009; `frontend-react/` con paridad funcional completa frente al Flet (feed, editor, mis gatos, auth, invitado→cuenta, perfil, configuración, stickers IA honesto, perfil público); gato SVG completo; iconos lucide; sonido Web Audio real; framer-motion; catálogo y API idénticos; CORS ampliado al puerto de Vite; evidencia en `docs/reports/frontend-react.md` | Alex Valdelamar |
| 2026-11-23 | Editor visual con SVG reales y multiaccesorio | Se actualizaron resumen, flujo, pantallas, arquitectura, modelo, motor y limitaciones: React usa cuerpo/cabello/prendas/accesorios reales, sliders, previews y grupos de compatibilidad. ADR-010, semilla de 53 códigos, esquema 1 aditivo y verificación en navegador/MySQL; evidencia en `docs/reports/editor-visual-assets.md` | Alex Valdelamar |
| 2026-11-23 | Color independiente por accesorio | Se documentó el mini slider en el borde inferior de cada tarjeta seleccionada, el color `accessories[].color`, su persistencia, la separación entre selección y slider y la compatibilidad del espejo legacy; ADR-010, OpenAPI, pruebas y evidencia actualizados | Alex Valdelamar |
| 2026-11-23 | Cabeza delantera y orden de capas | La cabeza base se integró sin perder el trabajo local y se renderiza después de la prenda superior; el cuerpo completo permanece atrás. Se documentaron anclajes, color de pelaje/ojos, lienzo sin recortes y verificación en lienzo y previews; ADR-010 y evidencia actualizados | Alex Valdelamar |
| 2026-11-23 | React como interfaz definitiva | ADR-011 sustituyó ADR-009; Flet y sus pruebas se retiraron del árbol activo. README, arquitectura, contratos, checklist, guía y evidencia pasaron a declarar React como única interfaz; los reportes Flet quedan como historial | Alex Valdelamar |

# Editor visual con assets reales — evidencia 2026-11-23

## Alcance

Se completó el editor React sobre los SVG entregados por diseño y se alineó el backend sin
romper el contrato de datos schema 1. React es la única interfaz activa; Flet se retiró por
[ADR-011](../decisions/ADR-011-react-interfaz-definitiva.md) y su evidencia es histórica.

- Registro de assets, anclajes y códigos reales en `frontend-react/src/lib/characters.ts`.
- Cabello dividido en capas trasera y delantera; cuerpo completo, inferior, superior, cabeza
  delantera y accesorios apilados en `frontend-react/src/components/CatSVG.tsx`.
- La cabeza se renderiza después de la prenda superior y antes del cabello delantero. Así,
  cuellos y solapas quedan detrás de la cara sin dividir ni regenerar el SVG del cuerpo.
- Sin texturas ni patrones de pelaje. Los SVG no añaden fondo blanco al lienzo.
- Sliders de color para cabello, parte superior y parte inferior. El primer cambio desde
  blanco, negro o gris introduce color visible.
- Mini slider de tono en el borde inferior de cada tarjeta de accesorio seleccionado; el color
  es independiente por accesorio y persiste en invitado y API.
- Previews SVG reales en cada botón de opción; preview y lienzo principal comparten el mismo
  renderizador.
- Múltiples accesorios con sustitución automática dentro del mismo `compatibility_group`;
  “Ninguno” vacía la lista.
- Configuración schema 1 con colores y `accessories[{code, color?}]`; `accessory: {code}` se
  mantiene como espejo legacy para datos y clientes antiguos
  ([ADR-010](../decisions/ADR-010-configuracion-visual-compatible.md)).
- Campo `catalog_options.compatibility_group`, migración no destructiva y semilla idempotente
  de 53 opciones y 6 poses.

## Verificación automatizada

| Comprobación | Resultado |
| --- | --- |
| `npm run build` | Correcto: 2580 módulos; bundle 800.21 kB (276.96 kB gzip). Aviso no bloqueante de chunk mayor de 500 kB. |
| `npm run lint` | 0 errores; 2 avisos `set-state-in-effect` ya conocidos en `PublicProfileScreen.tsx` y `EditorScreen.tsx`. |
| Backend con SQLite: `python -m pytest -q` en `backend/` | 66 pruebas aprobadas. |
| `python manage.py check` | Sin problemas. |
| `python manage.py makemigrations --check --dry-run` | Sin migraciones pendientes. |
| OpenAPI versionado | YAML y 25 esquemas válidos; 49 referencias locales resueltas. Validadas las formas canónica/legacy, `accessories[].color` de 6/8 dígitos, el rechazo de color inválido, la lista vacía sin espejo y las respuestas del hub. |
| Color en React | `#7B61FF80` se conserva al normalizar; `#abc` se expande a `#AABBCC`; un valor inválido usa el color de respaldo. |
| Assets SVG activos | 41 archivos XML válidos. Las clases de Illustrator se convierten a atributos en el render. |
| Flet | Interfaz y pruebas retiradas del árbol de entrega; las 46 pruebas históricas ya no forman parte de la verificación vigente. |

## Verificación en navegador

Página comprobada: `http://127.0.0.1:5173/crear`, modo invitado.

- Las seis pestañas están presentes. En “Superior” se mostraron seis previews SVG de 58 px y el
  slider de color.
- Interacción pointer real sobre el slider: cambió de `#7B61FF` a `#61A3FF`; el color apareció
  en nueve rellenos del lienzo principal.
- Al seleccionar “Manga corta” se conservó el color elegido y cambió la geometría de la prenda.
- Con “Bob”, las capas de cabello trasera y delantera tenían rutas distintas y compartieron el
  color `#54266B`.
- Se seleccionaron gafas, bigote, pipa y corona: el render pasó a tener diez capas (seis base +
  cuatro accesorios).
- Cambiar “Corona de 3” por “Corona de 4” mantuvo cuatro accesorios y sustituyó la corona.
  Cambiar gafas redondas por gafas grandes también sustituyó el accesorio del mismo grupo.
- “Ninguno” redujo el contador a cero y el render a seis capas base; “Deshacer” restauró la
  selección previa. “Aleatorio” produjo una combinación válida sin repetir grupos.
- Se guardó “QA editor visual” como invitado con colores y cuatro accesorios en `localStorage`.
  Tras recargar, apareció en “Mis gatos” con la configuración persistida y fue eliminado desde
  la interfaz.
- No quedaron gatos de prueba en el navegador (`kitchi.cats` quedó en cero).

## Corrección de la cabeza y del lienzo — 2026-11-23

Se integró `assets/characters/base/avatar_head.svg` sin sobrescribir los cambios locales. El
cuerpo completo se conserva como capa posterior y la cabeza se superpone después de la prenda
superior.

Orden comprobado:

1. Cabello trasero.
2. Cuerpo completo.
3. Prenda inferior.
4. Prenda superior.
5. Cabeza delantera.
6. Cabello delantero.
7. Accesorios, en el orden de selección.

Comprobaciones DOM sobre el lienzo y los seis previews:

- `viewBox`: `{x: 0, y: -10, width: 206.068, height: 270}`.
- Contenido principal: `{x: 2.732, y: -8.002, width: 190.705, height: 257.740}`.
- `insideViewBox: true` en el lienzo y en los seis previews; no se recortan pies, cabello ni
  accesorios.
- Cabeza: 16 paths, 2 ojos y transform `translate(6.745 15.722) scale(1.0000)`.
- Con “Puños” seleccionado hay siete capas: seis base y un accesorio. La cabeza mantiene el
  pelaje y el color de ojos, y el cuello de la prenda queda detrás de la cara.

Capturas limpias, sin credenciales ni datos de cuenta:

- [Lienzo completo con “Puños”](editor-head-2026-11-23.png).
- [Previews de la parte superior con “Puños” seleccionado](editor-head-options-2026-11-23.png).

La evidencia se obtuvo con interacciones reales, snapshots accesibles, evaluación DOM y
capturas del navegador. Las animaciones se reactivaron después de la comprobación.

## Verificación contra MySQL

Se creó una cuenta temporal y se usó su token de Django, sin registrar credenciales en la
evidencia.

| Operación | Resultado |
| --- | --- |
| Motor efectivo | `mysql` |
| `POST /api/cats/` con colores y cuatro accesorios | 201; configuración normalizada guardada |
| Accesorios devueltos | `round_glasses`, `bow_tie`, `moustache`, `three_pointed_crown` |
| Espejo legacy | `{"code": "round_glasses"}` |
| `PATCH /api/cats/{id}/` cambiando el color superior | 200; color actualizado a `#70D6C1` |
| `DELETE /api/cats/{id}/` | 204 |
| Limpieza | Gato, token y usuario temporal eliminados |

## Incremento de color por accesorio — 2026-11-23

### Navegador y modo invitado

- En “Extras” había dos accesorios seleccionados y exactamente dos mini sliders, uno en cada
  tarjeta seleccionada. Los controles no estaban anidados en botones (`button input = 0`) y
  quedaban dentro del borde inferior de la tarjeta.
- Una interacción real sobre el slider de “Gafas redondas” cambió el color de `#FCFCFC` a
  `#4BDDDD` (tono 180). El accesorio siguió seleccionado y el color apareció tanto en su preview
  como en el lienzo principal.
- El slider de “Corbata larga” se cambió por separado a `#4BDBDD`; las gafas conservaron
  `#4BDDDD`. Esto comprueba colores independientes y que arrastrar el control no selecciona ni
  quita el accesorio.
- Se guardó “QA colores accesorios” como invitado. `localStorage` registró
  `round_glasses: #4BDDDD` y `long_bow_tie: #4BDBDD`.
- Tras recargar, abrir “Mis gatos” y editar el personaje, el lienzo y ambos sliders recuperaron
  sus colores. El gato se eliminó desde la interfaz y `kitchi.cats` quedó en cero.

### MySQL y API

Se creó una cuenta temporal con correo `@example.test` y se eliminó al terminar; no se
registraron credenciales ni tokens en la evidencia.

| Comprobación | Resultado |
| --- | --- |
| Motor efectivo | `mysql` |
| `POST /api/cats/` con dos accesorios coloreados y espejo legacy | 201; colores guardados por separado |
| `GET /api/cats/{id}/` | 200; mismos colores al recuperar |
| `PATCH /api/cats/{id}/` cambiando solo el primer accesorio | 200; `#00AA88` y `#7B61FF80` conservados de forma independiente |
| Color de accesorio inválido | 400; error en `details.campos.accessories` |
| Espejo legacy | `{"code": "round_glasses"}` |
| `DELETE` + logout + eliminación de usuario temporal | 204 + 204; datos de prueba retirados |

## Pendiente honesto

- Completar `assets/catalog.json` con autoría, licencia y aprobación de recursos (P06/P08).
- La persistencia invitada depende de `localStorage`; no hay un respaldo garantizado en memoria
  si el navegador bloquea el almacenamiento. El manejo visible de ese caso queda en P39.
- El motor Pillow, los seis PNG exportables, los paquetes, la copia de publicaciones y la IA
  siguen pendientes (P13–P19).
- Falta verificar en vivo el comportamiento de un token inválido o expirado (P12/P39).
- Este incremento se entrega en la rama `feat/assets-personaje`; no se publica ni se hace push sin
  una autorización explícita para ello.

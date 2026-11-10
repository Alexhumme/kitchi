# Integración del frontend Flet con la API

Fecha: 9 de noviembre de 2026
Responsable: Martin Solano (frontend y UX)
Tareas relacionadas: P02, P08, P10, P12, P36, P39

## Objetivo

Conectar la interfaz Flet Web con la API REST existente para que el flujo de invitado y
cuenta use datos reales: catálogo, poses, registro, login, sesión y CRUD de gatos. No se
implementaron motores ni endpoints nuevos; lo que falta se muestra como pendiente.

## Entorno

- Windows, PowerShell 5.1.
- Backend: Django REST Framework sobre MySQL 8, servidor en `http://127.0.0.1:8000`.
- Frontend: Python 3.11.6 + Flet 1.1.2.
- Backend en marcha al ejecutar la verificación:
  `GET /api/health/` → `{"status":"ok","database":"up","engine":"mysql"}`.
- `.env` con `API_BASE_URL=http://127.0.0.1:8000` y CORS para
  `http://127.0.0.1:8550`.

## Cambios verificables

- `frontend/src/kitchi/api.py`: cliente HTTP con resolución de URL, token de Django,
  normalización de errores y métodos de cuentas, catálogo, poses, gatos y publicaciones.
- `frontend/src/kitchi/catalog.py`: catálogo dinámico desde el backend, adaptación de
  configuración normalizada y catálogo empaquetado de respaldo.
- `frontend/src/kitchi/storage.py`: persistencia de sesión además de los gatos de invitado.
- `frontend/src/kitchi/app.py`: arranque de sesión/catálogo/poses/gatos/publicaciones,
  login, logout, migración de gatos de invitado y mutaciones por API o local.
- `frontend/src/kitchi/screens/auth.py`: login y registro con validación, carga y errores.
- `frontend/src/kitchi/screens/profile.py`: identidad, sesión, estado de API/catálogo y datos.
- `frontend/src/kitchi/screens/editor.py`: previsualización provisional por capas de color,
  actualizada al cambiar la configuración.
- `frontend/src/kitchi/screens/hub.py`, `my_cats.py`, `stickers.py`: estados reales de API,
  publicaciones pendientes, poses reales y límites.
- `frontend/src/main.py` y `frontend/main.py`: punto de entrada documentado.
- `scripts/seed_catalog.py`: siembra idempotente de catálogo y poses provisionales.

## Catálogo sembrado

La API no tenía opciones ni poses, por lo que el editor no podía guardar gatos. Se ejecutó:

```bash
.venv\Scripts\python.exe scripts\seed_catalog.py
```

Resultado: **18 opciones** (3 por cada una de las 6 categorías) y **6 poses**. Las rutas
son `assets/placeholders/...`: son etiquetas de intención, **no archivos de imagen**. La API
las sirve en `/api/catalog/` y `/api/poses/` (este último paginado, `count: 6`).

## Pruebas ejecutadas

```bash
python -m compileall -q frontend scripts\seed_catalog.py
python -m pytest -q frontend\tests
```

Resultado: compilación sin errores y **34 pruebas en verde**. Cubren, entre otras cosas:

- Cliente HTTP en modo local y con URL.
- Payloads de registro, login y CRUD de gatos.
- Mensaje de error de campo y de catálogo (`ApiError.user_message`).
- Adaptación del catálogo del backend y rechazo de un catálogo vacío.
- Normalización de configuración y validación.
- Persistencia y limpieza de sesión; `cat_from_api`.
- Límite de tres gatos en invitado.

Además se ejecutó un smoke test con un `FakeApp` que construye las pantallas de hub, Mis
gatos, stickers, perfil, login, registro y el editor, y recorre todas las opciones del
catálogo. Resultado: `SMOKE OK`, sin excepciones de construcción de controles Flet.

También se levantó el servidor Flet Web con un script temporal que desactiva la apertura
del navegador (`webbrowser.open` sin efecto). `GET http://127.0.0.1:8550/` respondió **200**
y el proceso se detuvo al terminar. Esto comprueba el arranque del servidor y las
importaciones, no la interacción del cliente WebSocket.

Para confirmar que la API seguía sana después de los cambios se ejecutaron las pruebas del
backend y el verificador en vivo:

```bash
cd backend && python -m pytest -q        # 47 passed
cd .. && python scripts/check_backend.py # 19/19 comprobaciones superadas
```

`check_backend.py` autolimpió las cuentas y gatos temporales; no borra el catálogo sembrado.

## Lo que no se verificó

- No se hizo todavía un recorrido manual completo en el navegador (`http://127.0.0.1:8550/`)
  con backend real: registro, login, recarga de página y migración de gatos de invitado.
- No se probó el caso de token inválido o expirado en vivo.
- No existen assets finales ni motor Pillow; la previsualización es de color.
- No existen endpoints de paquetes, publicaciones ni IA; la interfaz los muestra como
  pendientes y no simula resultados.

## Conclusión

La integración de cuentas, catálogo, poses y gatos está implementada y cubierta por pruebas
automatizadas. El proyecto puede demostrar el editor y el guardado real; todavía no puede
demostrar generación de stickers, hub ni IA. Antes de la entrega falta la prueba manual en
navegador y sustituir los placeholders cuando lleguen los assets.

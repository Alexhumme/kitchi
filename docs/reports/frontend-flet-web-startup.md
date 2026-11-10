# Informe — arranque del frontend Flet Web y pantalla gris (2026-11-10)

**Autor:** Alex Valdelamar · **Versión afectada:** v0.2.0 · **Área:** frontend (Flet 1.1.2, web)

## El problema

1. Al abrir `flet run frontend/src/main.py --web` la página se veía completamente gris:
   sin cabecera, sin barra inferior y sin contenido; solo el color de fondo.
2. Cuando llegaba a leer el almacenamiento, el arranque moría con
   `RuntimeError: TimeoutException after 0:00:10.000000: Timeout waiting for invoke method listener for SharedPreferences(9).get`
   y la app nunca pintaba nada.

Ninguna de las dos tenía un error en Python que apuntara a la causa: era el cliente web de
Flet 1.1.2.

## Qué se hizo

Diagnóstico con navegador headless (CDP), bisecta incremental de la página y capturas de
pantalla:

- Causa 1: **iconos pasados como cadenas** (`ft.Icon("pets")`…). Flet 1.x exige
  `IconData` (`ft.Icons.PETS`); el cliente web no resuelve la cadena y el árbol de widgets
  falla al pintarse (en el build web, el widget de error es una caja gris).
- Causa 2: **`ft.Row(..., wrap=True)`**, propiedad válida en la API pero rota en el
  cliente 1.1.2 (misma caja gris).
- Causa 3: **carrera de arranque de `SharedPreferences`** (flet-dev/flet#6412).

Arreglos aplicados (registrados en [ADR-006](../decisions/ADR-006-flet-1-1-2-web-issues.md)):

- `frontend/src/kitchi/icons.py`: `icons.get(name)` resuelve nombres Material a `ft.Icons`
  con caché y `HELP_OUTLINE` como reserva; los componentes y las pantallas resuelven aquí.
- `frontend/src/kitchi/components.py`: `c.flow()` sustituye a `Row(wrap=True)` para las
  filas de chips; chips `dense` para las zonas estrechas del editor.
- `frontend/src/kitchi/storage.py`: `open_browser_storage()` crea una instancia nueva por
  intento, sondea con plazo de 1,2 s y devuelve `None` si no hay servicio utilizable.
- `frontend/src/kitchi/app.py`: la app pinta el armazón (cabecera + contenido + barra
  inferior) antes de tocar el almacenamiento; si el navegador no responde, sigue en memoria
  con un aviso visible en lugar de caerse. El arranque completo va envuelto para que un
  fallo parcial no impida usar la app.
- Migración de los iconos de todas las pantallas, botones, chips y barra inferior a
  `ft.Icons.*` / `icons.get(...)`.

## Verificación (evidencia)

- `python -m pytest -q` en `frontend/`: **42 pruebas pasan** (6 nuevas en
  `frontend/tests/test_startup.py` cubren el sondeo, los reintentos y el uso de memoria
  cuando el servicio no responde).
- Navegador real (Chrome headless + CDP, `http://127.0.0.1:8556/` servido con
  `flet_web.fastapi` y `assets_dir`):
  - Las cinco secciones (Navegar, Mis gatos, Crear, Stickers IA, Perfil) se pintan e
    interactúan; navegación por la barra inferior con coral en la activa y barra superior
    con nombre de cuenta/“Invitado”.
  - Creación de un gato como invitado (nombre “Azote”), guardado, **recarga de la página**
    y verificación en **Mis gatos**: “1/3” y el gato con su configuración (demuestra la
    lectura de `SharedPreferences` al arranque con el arreglo).
  - Conexión real con la API (`API_BASE_URL` del `.env`): “API conectada en
    http://127.0.0.1:8000.” en Perfil.
- Sin errores de `RuntimeException` ni páginas grises en ninguna carga controlada
  (más de 10 cargas frescas con perfil de navegador limpio).

## Capturas (adjunto)

| Archivo | Qué muestra |
| --- | --- |
| `flet-web-startup/navegar-home.png` | Sección Navegar: cabecera, hero con gradiente, pasos, barra inferior con iconos y "Navegar" seleccionada |
| `flet-web-startup/crear-editor.png` | Editor: gato placeholder, categorías laterales, chips de piezas y opciones de pelaje |
| `flet-web-startup/guardar-dialogo.png` | Diálogo "Guardar gato" con nombre y botones Cancelar/Guardar |
| `flet-web-startup/misgatos-tras-recarga.png` | Mis gatos tras recargar: "1/3" y el gato "Azote" con su configuración (persistencia en `SharedPreferences`) |
| `flet-web-startup/perfil-api-conectada.png` | Perfil con "API conectada en http://127.0.0.1:8000." |
| `flet-web-startup/stickers-ia.png` | Stickers IA: seis poses reales leídas de la API y el aviso honesto de generación pendiente |

## Qué queda pendiente

- El bug de `SharedPreferences` está **mitigado, no corregido**: al subir a una versión de
  Flet corregida conviene reevaluar (ver ADR-006).
- El editor sigue sin los assets de la diseñadora (P06) y sin render con Pillow (P13);
  la fila de piezas de “Sup. / Inf. / Extra” usa placeholders de color.
- La prueba del flujo completo con cuenta (login/registro contra la API verificado a mano)
  se ejecutó por automatización CDP y debe repetirse manualmente antes de la entrega (P36/P39).

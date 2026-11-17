# ADR-006 — Flet 1.1.2 (web): iconos, `Row(wrap=True)` y la carrera de `SharedPreferences`

- **Estado:** aceptado
- **Fecha:** 2026-11-10
- **Sustituye a:** —
- **Sustituida por:** —

## Contexto

La interfaz Flet Web arrancaba con la página completamente gris y ningún control
pintado, y el arranque fallaba con `RuntimeError: TimeoutException after … SharedPreferences(9).get`.
No había excepción en Python: era una combinación de comportamientos del cliente web de
Flet 1.1.2 que el modo debug tolera pero el build "release" oculta. En CanvasKit/Flutter web
el widget de error por defecto es una **caja gris**, por lo que cualquier error de construcción
en el árbol de widgets solo se ve como fondo gris y, en modo semántica activada, un árbol
v vacío.

Diagnóstico (navegador real, telemetría CDP y capturas):

1. **Iconos como cadenas.** Flet 1.x exige `IconDataOrControl` en
   `ft.Icon(…)`/iconos de controles. Pasar `"pets"` llega al cliente como un tipo no válido,
   el hijo falla al pintarse y toda la página queda en gris. Controles afectados: `ft.Icon`,
   `ft.IconButton`, `ft.Icons` en `ft.NavigationBarDestination`, etc.
2. **`ft.Row(wrap=True)`.** El cliente tampoco pinta el `Wrap` resultante; la página
   queda cubierta por la caja gris del widget de error. Afectaba a filas de chips y botones
   en la mayoría de las pantallas.
3. **`ft.SharedPreferences` al arrancar** (flet-dev/flet#6412). Esférico que registra el
   servicio antes de que el cliente monte su `ServiceRegistry`: el control existe pero no
   recibe listener; la primera lectura expira a los 10 s y mata el arranque.

## Decisión

- **Iconos siempre `ft.Icons.*` (IconData).** Para datos que siguen guardando nombres
  legibles (catálogo, poses, tablas de tonos) existe `kitchi/icons.get(name)`, un
  resolvedor con caché y `HELP_OUTLINE` como reserva; los componentes y pantallas pasan
  por él. No se admiten cadenas de icono en ningún control de Flet.
- **`Row(wrap=True)` prohibido.** Se añade `c.flow()` en
  `frontend/src/kitchi/components.py` (agrupa elementos en filas de a lo sumo `per_row`)
  para las filas de chips que deben fluir, y filas simples (o texto con salto de línea)
  en el resto.
- **El arranque pinta primero, persiste después.** `KitchiApp.start()` pinta el armazón
  (cabecera, contenido, barra inferior) y solo entonces crea el almacenamiento con
  `kitchi/storage.open_browser_storage()`: instancia nueva por intento, lectura de
  comprobación con plazo de 1,2 s y reintentos cortos. Si ninguna instancia responde se
  usa memoria y se muestra un aviso visible; la app nunca se cae.
- En pruebas se verificó el flujo real: crear un gato como invitado, recargar la página y
  verlo en **Mis gatos** (`1/3`); la lectura al arranque usa el mismo adaptador sondeado.

## Consecuencias

- **Positivas:** la app arranca siempre (degradar en lugar de tumbarse); pantallas
  completas e interactivamente verificadas en navegador; `Row` y chips funcionan;
  la paleta de iconos es explícita y se detectan nombres desconocidos en el log.
- **Negativas:** `c.flow()` no es un wrap real (filas de a lo sumo N elementos);
  las listas de chips necesitan estimar `per_row` según el ancho.
- **Riesgos:** el bug de `SharedPreferences` sigue abierto en Flet 1.1.2
  (flet-dev/flet#6412). La mitigación funciona, pero al subir de versión conviene
  reevaluar `open_browser_storage()` y quitar el sondeo.

## Alternativas descartadas

- **Esperar una versión Flet corregida.** No hay versión nueva (1.1.2 es la última).
- **Monkeypatch del cliente web o del paquete flet.** Cambios frágiles fuera del repo
  propio; no son mantenibles ni explicables en la sustentación.
- **Sustituir `SharedPreferences` por una API de sesión en la nube.** Fuera de alcance
  y contra el modo invitado sin cuenta.

## Verificación

- `pytest -q` en `frontend/`: 42 pruebas pasan, incluidas seis nuevas de arranque
  (`frontend/tests/test_startup.py`) que simulan un servicio que nunca responde y
  verifican el reintento y el uso de memoria.
- Navegador real (headless Chrome + CDP): recorrido por las cinco secciones, recarga
  con el gato guardado en modo invitado y persistencia confirmada; sin errores en consola
  ni pantalla gris.
- Informe completo en [`../reports/frontend-flet-web-startup.md`](../reports/frontend-flet-web-startup.md).

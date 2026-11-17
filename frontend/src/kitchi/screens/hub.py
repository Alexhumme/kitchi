"""Navegar / Explorar: feed público del hub con la cuadrícula de publicaciones (P18)."""

from __future__ import annotations

import asyncio

import flet as ft

from .. import components as c
from .. import icons
from .. import theme as t
from ..feed_ui import publication_card

_SEARCH_TOKEN = {"n": 0}


def _on_search_change(app, event=None, value: str | None = None) -> None:
    """Reinicia el feed ante cambios del buscador con debounce."""
    _SEARCH_TOKEN["n"] += 1
    token = _SEARCH_TOKEN["n"]
    if value is not None:
        app.feed_query = value.strip()
    elif event is not None and getattr(event, "control", None) is not None:
        app.feed_query = (event.control.value or "").strip()
    _reset_field_value(app)
    app.feed_page = 1

    async def _task() -> None:
        await asyncio.sleep(0.35)
        if token != _SEARCH_TOKEN["n"]:
            return
        app.feed_searching = True
        await app.refresh_feed(append=False)
        app.rebuild_current()

    app.page.run_task(_task)


def _reset_field_value(app) -> None:
    """Sincroniza el valor visible del campo con `app.feed_query`."""
    if app._search_field is None:
        return
    try:
        app._search_field.value = app.feed_query
    except Exception:  # noqa: BLE001 - el campo puede no estar montado durante el arranque
        pass


def _build_search_field(app) -> ft.Control:
    """La instancia proviene de app._search_field (se crea una sola vez).

    Flet destruye y recrea los controles en cada `rebuild_current()`; si el
    `TextField` se recrea, el cliente web pierde el teclado y no se puede
    escribir más en él. Por eso el campo vive en el app y se reutiliza.
    """
    field = app._search_field
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(icons.get("search"), size=20, color=t.TINTA),
                field,
                ft.IconButton(
                    icons.get("close"),
                    tooltip="Limpiar búsqueda",
                    icon_color=t.TINTA_SUAVE,
                    visible=bool(app.feed_query),
                    on_click=lambda e: _on_search_change(app, value=""),
                ),
            ],
            spacing=6,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.symmetric(horizontal=14, vertical=4),
        bgcolor=t.SUPERFICIE,
        border_radius=t.RADIO_PASTILLA,
        border=ft.Border.all(t.BORDE, t.TINTA),
        shadow=[t.SOMBRA],
    )


def _ensure_search_field(app) -> None:
    """Crea el TextField una sola vez y lo enlaza con el feed."""
    if app._search_field is not None:
        return

    def on_change(e):
        _on_search_change(app, event=e)

    app._search_field = ft.TextField(
        value=app.feed_query,
        hint_text="Buscar por creación o usuario…",
        border=ft.InputBorder.NONE,
        filled=False,
        dense=True,
        text_size=15,
        hint_style=ft.TextStyle(color=t.TINTA_SUAVE),
        cursor_color=t.TINTA,
        color=t.TINTA,
        on_change=on_change,
        expand=True,
    )


def _shimmer_grid() -> ft.Control:
    cells = [
        ft.Container(
            expand=1,
            height=180,
            border_radius=t.RADIO_GRANDE,
            bgcolor=t.CREMA_HONDO,
        )
        for _ in range(6)
    ]
    rows = [ft.Row(cells[i:i + 2], spacing=10) for i in range(0, len(cells), 2)]
    return ft.Shimmer(
        content=ft.Column(rows, spacing=10),
        highlight_color=t.SUPERFICIE,
        base_color=t.CREMA_HONDO,
    )


def _card_pair(first: ft.Control | None, second: ft.Control | None) -> ft.Control:
    return ft.Row(
        [first or ft.Container(expand=1), second or ft.Container(expand=1)],
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )


def _feed_grid(app) -> ft.Control:
    publications = app.publications
    rows = []
    for start in range(0, len(publications), 2):
        first = publication_card(app, publications[start])
        second = publication_card(app, publications[start + 1]) if start + 1 < len(publications) else None
        rows.append(_card_pair(first, second))
    load_more = None
    if app.feed_has_more:
        load_more = ft.Row(
            [ft.Container(
                content=c.secondary_button(
                    "Cargar más" if not app.feed_searching else "Cargando…",
                    app.load_more_feed if not app.feed_searching else None,
                    icon="expand_more",
                ),
            )],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    return ft.Column(rows + ([load_more] if load_more else []), spacing=10)


def _empty(app) -> ft.Control:
    if app.feed_error:
        return c.banner(app.feed_error, icon="info_outline", tone="warning")
    if app.feed_query:
        return c.empty_state(
            "search_off",
            "Nada por aquí",
            f"Ninguna creación coincide con «{app.feed_query}». Prueba con otro nombre o usuario.",
        )
    controls: list[ft.Control] = []
    if not app.user:
        controls.append(
            c.banner(
                "Inicia sesión para publicar tus propios gatos y seguir a otras personas.",
                icon="cloud_off",
                tone="info",
            )
        )
    controls.append(
        c.empty_state(
            "auto_awesome",
            "El feed está por estrenarse",
            "Todavía no hay creaciones públicas. Entra en Crear, guarda un gato y publícalo "
            "con el botón Publicar en Mis gatos."
            + (" Como invitado puedes crear y guardar, iniciar sesión para publicar." if not app.user else ""),
            c.primary_button("Crear mi gato", lambda e: app.go(2), icon="brush"),
        )
    )
    return ft.Column(controls, spacing=12)


def build(app) -> ft.Control:
    _ensure_search_field(app)
    return ft.Column(
        [
            _build_search_field(app),
            ft.Row(
                [
                    ft.Text(
                        (
                            f"{app.feed_total} publicación"
                            + ("s" if app.feed_total != 1 else "")
                            + " pública"
                            + ("s" if app.feed_total != 1 else "")
                        )
                        if app.api.mode == "http"
                        else "Modo local: el hub necesita conexión con la API",
                        size=12,
                        color=t.TINTA_SUAVE,
                    ),
                    ft.Container(expand=True),
                    c.chip(
                        "Actualizando…" if app.feed_searching else "Actualizado",
                        bgcolor=t.AMARILLO if app.feed_searching else t.MENTA,
                        color=t.TINTA,
                        dense=True,
                        icon="sync" if app.feed_searching else "check_circle",
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            _shimmer_grid() if app.feed_searching and not app.publications else (
                _feed_grid(app) if app.publications else _empty(app)
            ),
        ],
        spacing=10,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

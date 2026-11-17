"""Perfil público de un usuario: gatos publicados y sus publicaciones (P18).

Abierto desde las tarjetas del feed (enlace al autor). No requiere cuenta.
Se cachea una vez por perfil; al cerrar y volver se refresca la vista.
"""

from __future__ import annotations

import asyncio
import logging

import flet as ft

from .. import cat_view, catalog, components as c, icons, theme as t
from ..feed_ui import publication_card

logger = logging.getLogger(__name__)


def _back_row(app) -> ft.Control:
    return ft.Row(
        [
            ft.IconButton(
                icons.get("chevron_left"),
                tooltip="Volver",
                icon_color=t.TINTA,
                on_click=lambda e: app.close_public_profile(),
            ),
            ft.Text("Perfil público", style=t.section()),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def _shimmer() -> ft.Control:
    cells = [
        ft.Container(expand=1, height=160, border_radius=t.RADIO_GRANDE, bgcolor=t.CREMA_HONDO)
        for _ in range(6)
    ]
    rows = [ft.Row(cells[i:i + 2], spacing=10) for i in range(0, len(cells), 2)]
    return ft.Shimmer(
        content=ft.Column(rows, spacing=10),
        highlight_color=t.SUPERFICIE,
        base_color=t.CREMA_HONDO,
    )


async def _load_profile(app, username: str) -> None:
    from ..api import ApiError

    try:
        payload = await asyncio.to_thread(app.api.get_public_profile, username)
    except ApiError as exc:
        app._public_profile_cache = {"username": username, "data": None, "error": exc.user_message()}
        app.rebuild_current()
        return
    app._public_profile_cache = {"username": username, "data": payload, "error": None}
    app.rebuild_current()


def _grid(cards: list[ft.Control]) -> ft.Control:
    rows = []
    for start in range(0, len(cards), 2):
        first = cards[start]
        second = cards[start + 1] if start + 1 < len(cards) else None
        rows.append(ft.Row([first, second or ft.Container(expand=1)], spacing=10))
    return ft.Column(rows, spacing=10)


def _render(app, data: dict) -> ft.Control:
    publications = data.get("publications") or []
    cats = data.get("cats") or []
    joined = data.get("joined_at") or ""

    cats_section = ft.Container()
    if cats:
        previews = [
            ft.Container(
                content=cat_view.cat_face(catalog.normalize_configuration(cat.get("configuration") or {}), 56),
                width=56,
                height=56,
                bgcolor=t.CREMA_HONDO,
                border_radius=t.RADIO_MEDIO,
                alignment=ft.Alignment.CENTER,
                tooltip=cat.get("name") or "",
            )
            for cat in cats
        ]
        cats_section = c.card(
            ft.Column(
                [
                    c.section_title("Gatos publicados", "Los que esta persona ha publicado en el hub"),
                    ft.Row(previews, spacing=10, wrap=False),
                ],
                spacing=8,
            ),
            padding=14,
        )

    cards = [publication_card(app, pub) for pub in publications]
    posts_section = c.card(
        ft.Column(
            [
                c.section_title("Publicaciones", f"{len(publications)} publicación{'es' if len(publications) != 1 else ''} pública{'s' if len(publications) != 1 else ''}"),
                _grid(cards) if cards else ft.Text("Sin publicaciones públicas todavía.", style=t.caption()),
            ],
            spacing=8,
        ),
        padding=14,
    )

    return ft.Column(
        [
            _back_row(app),
            c.card(
                ft.Row(
                    [
                        c.avatar(data.get("username") or "?", size=64),
                        ft.Column(
                            [
                                ft.Text(data.get("username") or "?", size=22, weight=ft.FontWeight.W_800, color=t.TINTA),
                                c.chip(
                                    f"Miembro desde {joined}" if joined else "Miembro",
                                    icon="event",
                                    dense=True,
                                    bgcolor=t.CREMA_HONDO,
                                ),
                                ft.Text(
                                    f"{data.get('publication_count', 0)} publicación{'es' if data.get('publication_count', 0) != 1 else ''} pública{'s' if data.get('publication_count', 0) != 1 else ''}",
                                    style=t.caption(),
                                ),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                    ],
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=16,
            ),
            cats_section,
            posts_section,
        ],
        spacing=12,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )


def build(app, username: str) -> ft.Control:
    cache = getattr(app, "_public_profile_cache", None) if app else None
    if cache and cache.get("username") == username:
        if cache.get("error"):
            return c.banner(f"No se pudo abrir el perfil: {cache['error']}", icon="info_outline", tone="warning")
        if cache.get("data") is not None:
            return _render(app, cache["data"])
    app.page.run_task(_load_profile, app, username)
    return ft.Column(
        [
            _back_row(app),
            ft.Shimmer(
                content=ft.Container(height=160, bgcolor=t.CREMA_HONDO, border_radius=t.RADIO_GRANDE),
                highlight_color=t.SUPERFICIE,
                base_color=t.CREMA_HONDO,
            ),
            _shimmer(),
        ],
        spacing=12,
        expand=True,
    )

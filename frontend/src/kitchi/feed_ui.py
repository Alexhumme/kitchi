"""Piezas compartidas del feed del hub (P18): tarjeta cuadrada."""

from __future__ import annotations

import flet as ft

from . import cat_view, catalog, components as c, icons, theme as t

PREVIEW_HEIGHT = 118


def author_row(app, username: str, size: int = 18) -> ft.Control:
    """Fila de autor clicable: avatar con inicial + nombre."""
    return ft.Row(
        [
            c.avatar(username, size=size),
            ft.TextButton(
                content=ft.Text(
                    username,
                    size=11,
                    weight=ft.FontWeight.W_600,
                    color=t.TINTA,
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                on_click=lambda _e, name=username: app.open_public_profile(name),
            ),
        ],
        spacing=6,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def publication_card(app, publication: dict) -> ft.Control:
    """Tarjeta cuadrada del feed: preview, título y autor."""
    cat = publication.get("cat") or {}
    configuration = catalog.normalize_configuration(cat.get("configuration") or {})
    title = publication.get("title") or cat.get("name") or "Sin título"
    return ft.Container(
        expand=1,
        content=ft.Column(
            [
                ft.Container(
                    content=cat_view.cat_face(configuration, 96),
                    height=PREVIEW_HEIGHT,
                    width=float("inf"),
                    bgcolor=t.CREMA_HONDO,
                    border_radius=t.RADIO_MEDIO,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Text(
                    title,
                    size=13,
                    weight=ft.FontWeight.W_700,
                    color=t.TINTA,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                author_row(app, publication.get("author") or "?"),
            ],
            spacing=6,
            tight=True,
        ),
        padding=ft.Padding.symmetric(horizontal=8, vertical=8),
        bgcolor=t.SUPERFICIE,
        border_radius=t.RADIO_GRANDE,
        border=ft.Border.all(t.BORDE, t.TINTA),
        shadow=[t.SOMBRA],
        tooltip=title,
    )

"""Navegar / Explorar: bienvenida, flujo del producto y estado del hub."""

from __future__ import annotations

import flet as ft

from .. import components as c
from .. import theme as t


def build(app) -> ft.Control:
    hero = ft.Container(
        content=ft.Column(
            [
                c.chip(
                    f"API conectada · {app.user.get('username')}" if app.api_online and app.user
                    else ("API conectada" if app.api_online else "Modo local"),
                    bgcolor="#FFFFFF66",
                    color=t.TINTA,
                    icon="cloud_done" if app.api_online else "cloud_off",
                ),
                ft.Text("kitchi.studio", size=32, weight=ft.FontWeight.W_700, color=t.TINTA),
                ft.Text("Caos adorable, a tu manera", size=18, weight=ft.FontWeight.W_500, color=t.TINTA),
                ft.Text(
                    "Diseña un gato chibi pieza a pieza, guárdalo en tu cuenta o en este "
                    "navegador y prepárate para compartirlo.",
                    size=14,
                    color=t.TINTA,
                ),
                ft.Row(
                    [
                        c.primary_button("Crear mi gato", lambda e: app.go(2), icon="brush"),
                        c.secondary_button("Mis gatos", lambda e: app.go(1), icon="pets"),
                    ],
                    spacing=8,
                    wrap=True,
                ),
            ],
            spacing=10,
        ),
        padding=22,
        border_radius=24,
        gradient=ft.LinearGradient(
            colors=[t.MELOCOTON, t.ROSA, t.LAVANDA],
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
        ),
    )

    steps = ft.Column(
        [
            c.section_title("Así funciona", "Tres pasos, cero talento requerido"),
            _step("1", "Elige tus piezas", "Seis categorías, tres opciones cada una. Pelaje, ojos, cabello, ropa y extras.", "palette"),
            _step("2", "Combina sin miedo", "Cambia lo que quieras en tiempo real y deshaz cuando el caos se pase de la raya.", "casino"),
            _step("3", "Guarda y comparte", "Guarda hasta 3 gatos por cuenta o en este navegador. El hub llega con P18.", "pets"),
        ],
        spacing=10,
    )

    return ft.Column(
        [hero, steps, _community(app)],
        spacing=18,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


def _community(app) -> ft.Control:
    body: list[ft.Control] = [
        ft.Row(
            [
                ft.Icon("explore_outlined", size=22, color=t.VIOLETA),
                ft.Text("Hub comunitario", style=t.section()),
                c.chip("P18" if not app.publications else f"{len(app.publications)}", bgcolor=t.LAVANDA),
            ],
            spacing=8,
        )
    ]

    if app.publications:
        for publication in app.publications:
            body.append(_publication_row(publication))
    else:
        body.append(
            ft.Text(
                "Aquí podrás explorar creaciones de otras personas, publicar las tuyas "
                "y copiar cualquier gato público para remixearlo.",
                style=t.body(),
            )
        )
        body.append(
            ft.Row(
                [
                    c.chip("Publicar", icon="share"),
                    c.chip("Explorar", icon="search"),
                    c.chip("Copiar", icon="copy_all"),
                ],
                spacing=8,
                wrap=True,
            )
        )
        if not app.api_online:
            body.append(
                c.banner(
                    "La API no está conectada: el hub no puede cargar publicaciones.",
                    icon="cloud_off",
                    tone="warning",
                )
            )
        else:
            detail = app.publications_error or "No hay publicaciones públicas todavía."
            body.append(
                c.banner(
                    f"{detail} Publicar y copiar se activan cuando el backend exponga "
                    "/api/publications/ (P18/P19).",
                    icon="info_outline",
                )
            )
    return c.card(ft.Column(body, spacing=12))


def _publication_row(publication: dict) -> ft.Control:
    title = publication.get("title") or publication.get("name") or "Creación pública"
    description = publication.get("description") or ""
    author = publication.get("username") or publication.get("author") or publication.get("user") or ""
    return c.card(
        ft.Column(
            [
                ft.Text(title, size=15, weight=ft.FontWeight.W_600, color=t.TINTA),
                ft.Text(f"Por {author}" if author else "Creación de la comunidad", style=t.caption()),
                ft.Text(description, style=t.body()) if description else ft.Container(),
                c.secondary_button("Copiar (P19)", None, icon="copy_all", disabled=True),
            ],
            spacing=6,
        ),
        padding=12,
    )


def _step(number: str, title: str, body: str, icon: str) -> ft.Container:
    return c.card(
        ft.Row(
            [
                ft.Container(
                    content=ft.Text(number, size=18, weight=ft.FontWeight.W_700, color="#FFFFFF"),
                    width=36,
                    height=36,
                    bgcolor=t.CORAL,
                    border_radius=18,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Column(
                    [
                        ft.Text(title, size=15, weight=ft.FontWeight.W_600, color=t.TINTA),
                        ft.Text(body, style=t.caption()),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.Icon(icon, size=22, color=t.TINTA_SUAVE),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=14,
    )

"""Navegar / Explorar: bienvenida, flujo del producto y estado del hub."""

from __future__ import annotations

import flet as ft

from .. import components as c
from .. import theme as t


def build(app) -> ft.Control:
    hero = ft.Container(
        content=ft.Column(
            [
                c.chip("Prototipo MVP · semana 2", bgcolor="#FFFFFF66", color=t.TINTA),
                ft.Text("kitchi.studio", size=32, weight=ft.FontWeight.W_700, color=t.TINTA),
                ft.Text("Caos adorable, a tu manera", size=18, weight=ft.FontWeight.W_500, color=t.TINTA),
                ft.Text(
                    "Diseña un gato chibi pieza a pieza, guarda tus creaciones "
                    "y prepárate para compartirlas.",
                    size=14,
                    color=t.TINTA,
                ),
                ft.Container(
                    c.primary_button("Crear mi gato", lambda e: app.go(2), icon="brush"),
                    padding=ft.Padding.only(top=8),
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
            _step("2", "Combina sin miedo", "Cambia lo que quieras en tiempo real y deshace cuando el caos se pase de la raya.", "casino"),
            _step("3", "Guarda y comparte", "Guarda hasta 3 gatos en este dispositivo. El hub llegará con la semana 3.", "pets"),
        ],
        spacing=10,
    )

    community = c.card(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon("explore_outlined", size=22, color=t.VIOLETA),
                        ft.Text("Hub comunitario", style=t.section()),
                        c.chip("Semana 3", bgcolor=t.LAVANDA),
                    ],
                    spacing=8,
                ),
                ft.Text(
                    "Aquí podrás explorar creaciones de otras personas, publicar las tuyas "
                    "y copiar cualquier gato público para remixearlo.",
                    style=t.body(),
                ),
                ft.Row(
                    [
                        c.chip("Publicar", icon="share"),
                        c.chip("Explorar", icon="search"),
                        c.chip("Copiar", icon="copy_all"),
                    ],
                    spacing=8,
                    wrap=True,
                ),
                c.banner(
                    "El hub se activa cuando el backend implemente publicaciones (P18). "
                    "Sin datos simulados: este espacio estará vacío hasta entonces.",
                    icon="info_outline",
                ),
            ],
            spacing=12,
        )
    )

    return ft.Column(
        [hero, steps, community],
        spacing=18,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
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
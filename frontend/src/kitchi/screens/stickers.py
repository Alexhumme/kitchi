"""Stickers IA: flujo de generación de seis poses.

La generación real vive en el backend/motor (P13–P16, semana 3). Esta pantalla
muestra el flujo acordado y sus estados, sin simular resultados.
"""

from __future__ import annotations

import flet as ft

from .. import components as c
from .. import theme as t

POSES = (
    ("greeting", "Saludo"),
    ("happy", "Alegría"),
    ("angry", "Enfado"),
    ("sad", "Tristeza"),
    ("surprised", "Sorpresa"),
    ("sleepy", "Sueño"),
)


def build(app) -> ft.Control:
    cats = app.cats
    cat_names = [cat["name"] for cat in cats]

    picker = ft.Dropdown(
        label="Gato de partida",
        hint_text="Elige un gato guardado" if cats else "Primero guarda un gato",
        options=[ft.dropdown.Option(name) for name in cat_names],
        disabled=not cats,
        border_radius=14,
        bgcolor=t.SUPERFICIE,
        expand=True,
    )

    flow = c.card(
        ft.Column(
            [
                c.section_title("El paquete", "Seis stickers PNG con fondo transparente"),
                ft.Row(
                    [c.chip(name, bgcolor=t.CREMA_HONDO, icon="emoji_emotions") for _, name in POSES],
                    spacing=6,
                    wrap=True,
                    run_spacing=6,
                ),
                ft.Text(
                    "El motor compondrá tu gato en las seis poses y podrás descargar "
                    "cada PNG o el paquete completo.",
                    style=t.body(),
                ),
            ],
            spacing=10,
        )
    )

    status = c.card(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon("auto_awesome", size=22, color=t.VIOLETA),
                        ft.Text("Generación: semana 3", style=t.section()),
                        c.chip("P13–P16", bgcolor=t.LAVANDA),
                    ],
                    spacing=8,
                ),
                ft.Text(
                    "El motor gráfico (Pillow), el seguimiento de trabajos y la integración "
                    "de IA se implementan en la semana 3. Aquí verás el progreso real: "
                    "pendiente, en proceso, completado o fallido.",
                    style=t.body(),
                ),
                c.banner(
                    "Nada se genera todavía: este botón se activará cuando el backend "
                    "exponga /api/sticker-packs/ y /api/ai-jobs/.",
                    icon="info_outline",
                ),
            ],
            spacing=10,
        )
    )

    action = ft.Column(
        [
            picker,
            c.primary_button("Generar 6 stickers", None, icon="auto_awesome", disabled=True, expand=True),
            ft.Text(
                "Disponible cuando exista el motor de generación." if cats
                else "Guarda un gato en el editor para poder generar su paquete.",
                style=t.caption(),
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        spacing=8,
    )

    return ft.Column(
        [c.section_title("Stickers IA", "De tu gato a un paquete compartible"), flow, status, action],
        spacing=14,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
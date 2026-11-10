"""Stickers IA: flujo de generación de seis poses.

La generación real vive en el backend/motor (P13–P16, semana 3). Esta pantalla
muestra las poses reales que expone la API y los estados del flujo, sin simular
resultados.
"""

from __future__ import annotations

import flet as ft

from .. import components as c
from .. import theme as t


def build(app) -> ft.Control:
    cats = app.cats
    cat_names = [cat["name"] for cat in cats]
    poses = app.poses or []

    picker = ft.Dropdown(
        label="Gato de partida",
        hint_text="Elige un gato guardado" if cats else "Primero guarda un gato",
        options=[ft.dropdown.Option(name) for name in cat_names],
        disabled=not cats,
        border_radius=14,
        bgcolor=t.SUPERFICIE,
        expand=True,
    )

    pose_chips = [c.chip(pose.get("name") or pose.get("code"), bgcolor=t.CREMA_HONDO,
                         icon="emoji_emotions") for pose in poses]
    flow = c.card(
        ft.Column(
            [
                c.section_title("El paquete", "Seis stickers PNG con fondo transparente"),
                ft.Row(pose_chips, spacing=6, wrap=True, run_spacing=6) if pose_chips
                else c.banner("La API no devolvió poses activas. Ejecuta scripts/seed_catalog.py.",
                              icon="warning_amber", tone="warning"),
                ft.Text(
                    f"{len(poses)} poses cargadas desde /api/poses/." if app.api_online and poses
                    else "Poses empaquetadas para el modo local.",
                    style=t.caption(),
                ),
                ft.Text(
                    "El motor compondrá tu gato en las seis poses y podrás descargar "
                    "cada PNG o el paquete completo. Mientras no existan los assets se "
                    "usará el mismo placeholder de color del editor.",
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
                        ft.Text("Generación pendiente (semana 3)", style=t.section()),
                        c.chip("P13–P16", bgcolor=t.LAVANDA),
                    ],
                    spacing=8,
                ),
                ft.Text(
                    "El motor gráfico (Pillow), el seguimiento de trabajos y la integración "
                    "de IA aún no están implementados. Aquí verás el progreso real: "
                    "pendiente, en proceso, completado o fallido.",
                    style=t.body(),
                ),
                c.banner(
                    "Nada se genera todavía: faltan /api/sticker-packs/ y /api/ai-jobs/ "
                    "en el backend. La pantalla no simula resultados.",
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

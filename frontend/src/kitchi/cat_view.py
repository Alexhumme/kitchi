"""Render provisional de un gato chibi con placeholders de color.

Es la misma lógica que usa el editor (`screens/editor.py`), empaquetada para
tamaños pequeños y sin interactividad: tarjetas del feed, perfil público y
agrupador de Mis gatos. Cuando lleguen los assets definitivos (P06/P08) esta
capa se sustituye por el render real de Pillow.
"""

from __future__ import annotations

import flet as ft

from . import catalog
from . import theme as t

SIZES = {
    "card": 96,      # tarjetas del feed (cuadrado 2 columnas)
    "grid": 128,     # gatos en perfil público
    "thumb": 56,     # miniatura en filas/listados
}


def _option(configuration: dict, key: str):
    return catalog.get_option(key, configuration.get(key, ""))


def cat_face(configuration: dict, size: int = 96) -> ft.Control:
    """Cara de gato del color del catálogo; si falta algo, texto honesto."""
    fur = _option(configuration, "fur")
    eyes = _option(configuration, "eyes")
    hair = _option(configuration, "hair")
    top = _option(configuration, "top")
    bottom = _option(configuration, "bottom")
    accessory = _option(configuration, "accessory")
    if not all((fur, eyes, hair, top, bottom, accessory)):
        return ft.Text("?", size=size // 2, color=t.TINTA_SUAVE)

    k = size / 200  # lienzo base ~200px

    def eye() -> ft.Container:
        width = int(18 * k) or 4
        eye_w = int(22 * k) if eyes.code == "round_green" else (int(26 * k) if eyes.code == "big_blue" else int(28 * k))
        eye_h = eye_w if eyes.code != "almond_amber" else max(4, int(15 * k))
        return ft.Container(
            content=ft.Container(
                width=max(2, int(eye_w * 0.4)),
                height=max(2, int(eye_w * 0.4)),
                bgcolor=t.TINTA,
                border_radius=100,
            ),
            width=eye_w,
            height=eye_h,
            bgcolor=eyes.swatch,
            border=ft.Border.all(max(1, int(2 * k)), t.TINTA),
            border_radius=100,
            alignment=ft.Alignment.CENTER,
        )

    ears = [
        ft.Container(width=int(52 * k), height=int(52 * k), bgcolor=fur.swatch,
                     border=ft.Border.all(max(1, int(2 * k)), t.TINTA),
                     border_radius=int(18 * k), left=int(32 * k), top=int(16 * k)),
        ft.Container(width=int(52 * k), height=int(52 * k), bgcolor=fur.swatch,
                     border=ft.Border.all(max(1, int(2 * k)), t.TINTA),
                     border_radius=int(18 * k), right=int(32 * k), top=int(16 * k)),
    ]
    stack = ft.Stack(
        [
            *ears,
            ft.Container(width=int(178 * k), height=int(154 * k), bgcolor=fur.swatch,
                         border=ft.Border.all(max(1, int(2 * k)), t.TINTA),
                         border_radius=int(80 * k), left=int(26 * k), top=int(34 * k)),
            ft.Container(width=int(128 * k), height=int(36 * k), bgcolor=hair.swatch,
                         border=ft.Border.all(max(1, int(1.5 * k)), t.TINTA),
                         border_radius=int(18 * k), left=int(51 * k), top=int(41 * k)),
            ft.Container(
                content=ft.Row([eye(), eye()], spacing=int(22 * k),
                                alignment=ft.MainAxisAlignment.CENTER),
                width=int(110 * k), left=int(60 * k), top=int(100 * k),
            ),
            ft.Container(
                width=max(4, int(12 * k)), height=max(3, int(8 * k)),
                bgcolor=t.CORAL, border_radius=6, left=int(109 * k), top=int(150 * k),
            ),
        ],
        width=int(220 * k),
        height=int(200 * k),
    )
    return ft.Container(
        content=stack,
        width=int(220 * k),
        height=int(200 * k),
        alignment=ft.Alignment.CENTER,
    )

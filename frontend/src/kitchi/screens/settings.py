"""Configuración de la app: acerca de, efectos, API y datos locales."""

from __future__ import annotations

import flet as ft

from .. import components as c
from .. import icons
from .. import theme as t

APP_VERSION = "0.3.0"


def _toggle_row(app, *, icon: str, title: str, caption: str, value: bool,
                on_change, disabled: bool = False) -> ft.Control:
    switch = ft.Switch(
        value=value,
        on_change=on_change,
        active_color=t.CORAL,
        disabled=disabled,
    )
    return ft.Row(
        [
            ft.Icon(icons.get(icon), size=22, color=t.TINTA),
            ft.Column(
                [
                    ft.Text(title, size=14, weight=ft.FontWeight.W_600, color=t.TINTA),
                    ft.Text(caption, style=t.caption()),
                ],
                spacing=0,
                expand=True,
            ),
            switch,
        ],
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def _info_row(*, icon: str, text: str) -> ft.Control:
    return ft.Row(
        [
            ft.Icon(icons.get(icon), size=20, color=t.TINTA_SUAVE),
            ft.Text(text, size=12, color=t.TINTA_SUAVE, expand=True),
        ],
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def build(app) -> ft.Control:
    page = app.page

    toggles = [
        _toggle_row(
            app,
            icon="animation",
            title="Animaciones",
            caption="Rebote al tocar botones y controles, y fundidos al cambiar de sección.",
            value=app.animations_enabled,
            on_change=lambda e: app.page.run_task(app.set_animations_enabled, e.control.value),
        ),
        _toggle_row(
            app,
            icon="vibration",
            title="Vibración táctil (solo móvil)",
            caption="Impulso breve al tocar botones y navegar. En web no hace nada.",
            value=getattr(app, "haptic_enabled", True),
            on_change=lambda e: app.page.run_task(app.set_haptic_enabled, e.control.value),
        ),
    ]

    api_status = _api_status(app)

    def on_sound(_e):
        c.notify(app.page, "Flet 1.1.2 no puede reproducir audio; el sonido llegará con una versión que lo incluya.", "info")

    return ft.Column(
        [
            c.app_bar(
                "Configuración",
                on_back=lambda e: app.close_settings(),
                subtitle="acerca de la app, sus efectos y datos",
                right=c.chip(f"v{APP_VERSION}", bgcolor=t.LAVANDA, icon="cable"),
            ),
            c.pattern_card(
                ft.Column(
                    [
                        ft.Icon(icons.get("pets"), size=44, color=t.CORAL),
                        ft.Text("kitchi.studio", size=28, weight=ft.FontWeight.W_800, color=t.TINTA),
                        ft.Text("Caos adorable, a tu manera", size=15, weight=ft.FontWeight.W_600, color=t.TINTA_SUAVE),
                        ft.Text(
                            "Compón un gato chibi pieza a pieza, guárdalo en tu cuenta o en este navegador, "
                            "publícalo en el hub y prepárate para llevarte el paquete de seis stickers.",
                            style=t.body(),
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Row(
                            [c.chip("Flet Web", icon="open_in_browser", dense=True),
                             c.chip("Django REST", icon="api", dense=True),
                             c.chip("Fredoka", icon="text_fields", dense=True)],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        ft.Text(
                            "Los gatos se muestran con placeholders de color hasta que lleguen los assets de la "
                            "diseñadora (P06/P08) y el render con Pillow (P13/P14).",
                            size=11,
                            color=t.TINTA_SUAVE,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=22,
                pattern="checker_soft",
                surface_alpha=0.84,
            ),
            c.pattern_card(
                ft.Column(
                    [
                        c.section_title("Así funciona", "Tres pasos, cero talento requerido"),
                        _step("1", "Elige tus piezas", "Seis categorías, tres opciones cada una. Pelaje, ojos, cabello, ropa y extras.", "palette"),
                        _step("2", "Combina sin miedo", "Cambia lo que quieras en tiempo real y deshaz cuando el caos se pase de la raya.", "casino"),
                        _step("3", "Guarda y comparte", "Guarda hasta 3 gatos por cuenta o en este navegador; publícalo en el hub.", "pets"),
                    ],
                    spacing=10,
                ),
                padding=16,
                pattern="dots_soft",
                surface_alpha=0.84,
            ),
            c.pattern_card(
                ft.Column(
                    [
                        c.section_title("Efectos"),
                        *toggles,
                        c.banner(
                            "El sonido de la app llegará cuando Flet incorpore reproducción de audio "
                            "(la versión 1.1.2 no la incluye); hoy la app se siente física con rebotes y vibración.",
                            icon="volume_up",
                            tone="info",
                        ),
                    ],
                    spacing=12,
                ),
                padding=16,
                pattern="crosshatch",
                surface_alpha=0.84,
            ),
            api_status,
            c.divider("zigzag"),
            c.card(
                ft.Column(
                    [
                        c.section_title("Tus datos"),
                        ft.Text(
                            "Vacía los gatos guardados en este navegador. Si tienes cuenta, los de la API no se tocan.",
                            style=t.caption(),
                        ),
                        c.secondary_button(
                            "Vaciar datos locales",
                            app.ask_clear_local,
                            icon="delete_outline",
                        ),
                    ],
                    spacing=8,
                ),
                padding=16,
            ),
            c.card(
                ft.Column(
                    [
                        c.section_title("Acerca de"),
                        _info_row(icon="copyright", text="Kitchi Studio — Programación Avanzada A1 · 2026-2"),
                        _info_row(icon="article", text="Tipografía Fredoka bajo licencia OFL. Placeholders de color hasta las entregas gráficas."),
                        _info_row(icon="code", text="Flet 1.1.2 (web), Django REST Framework, MySQL 8. Código abierto dentro del repo del curso."),
                    ],
                    spacing=8,
                ),
                padding=16,
            ),
        ],
        spacing=12,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )


def _step(number: str, title: str, body: str, icon: str) -> ft.Container:
    return c.card(
        ft.Row(
            [
                ft.Container(
                    content=ft.Text(number, size=18, weight=ft.FontWeight.W_800, color="#FFFFFF"),
                    width=36,
                    height=36,
                    bgcolor=t.CORAL,
                    border_radius=18,
                    border=t.bevel(t.INK, right=3, bottom=4),
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Column(
                    [
                        ft.Text(title, size=15, weight=ft.FontWeight.W_700, color=t.TINTA),
                        ft.Text(body, style=t.caption()),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.Icon(icons.get(icon), size=22, color=t.TINTA_SUAVE),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=14,
    )


def _api_status(app) -> ft.Control:
    if app.api_online:
        tone, icon, text = "success", "cloud_done", f"API conectada en {app.api.base_url}."
    elif app.api.mode == "local":
        tone, icon, text = (
            "warning",
            "cloud_off",
            "Sin API configurada: la app usa el catálogo empaquetado y el almacenamiento local. "
            "Define API_BASE_URL en el .env para conectar.",
        )
    else:
        tone, icon = "error", "cloud_off"
        detail = app.api_error or "No se pudo contactar el servidor."
        text = f"API no disponible en {app.api.base_url}. {detail}"

    catalog_text = (
        "Catálogo servido por /api/catalog/."
        if app.catalog_source == "api"
        else "Catálogo provisional empaquetado; ejecuta scripts/seed_catalog.py para sembrar la API."
    )
    return c.card(
        ft.Column(
            [
                c.section_title("Estado de la API", "Estado real, sin datos simulados"),
                c.banner(text, icon=icon, tone=tone),
                c.banner(catalog_text, icon="inventory_2", tone="info" if app.catalog_source == "api" else "warning"),
            ],
            spacing=8,
        ),
        padding=16,
    )

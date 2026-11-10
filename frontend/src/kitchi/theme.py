"""Sistema de diseño de Kitchi Studio.

Dirección híbrida acordada con frontend/UX:
- Base crema + tinta (directrices de marca) para superficies y texto.
- Coral del kit UI/UX reservado a acciones principales y selección activa.
- Una sola familia tipográfica: Fredoka (jerarquías por peso).

Los acentos (violeta, amarillo, menta, melocotón, rosa, lavanda) se usan con
moderación para no competir con el personaje. El color nunca es el único
indicador de estado: se acompaña de icono, etiqueta o contorno.
"""

from __future__ import annotations

import flet as ft

# --- Paleta -------------------------------------------------------------
CREMA = "#FFF3DF"        # fondo principal
CREMA_HONDO = "#FBEBCE"  # superficie cálida secundaria
SUPERFICIE = "#FFFBF2"   # tarjetas
TINTA = "#302B3A"        # texto / contornos
TINTA_SUAVE = "#6B6478"  # texto secundario (contraste sobre crema)

CORAL = "#FF6B6B"        # acción principal / selección activa
CORAL_HONDO = "#E45555"  # pressed / énfasis
CORAL_SUAVE = "#FFE3E0"  # fondo de selección

AMARILLO = "#FFD166"     # destacados / advertencia suave
VIOLETA = "#7B61FF"      # acento secundario / info
MENTA = "#70D6C1"        # éxito
MENTA_HONDA = "#2F9E8B"  # texto de éxito con contraste
MELOCOTON = "#FFB997"    # acento cálido
ROSA = "#F7D7E8"         # detalle decorativo
LAVANDA = "#DBC6FF"      # degradados puntuales
GRIS_CALIDO = "#EAE6DD"  # bordes / divisores

# Semánticos
EXITO = MENTA_HONDA
ADVERTENCIA = "#B07A1E"
ERROR = "#D64545"
INFO = VIOLETA

FONT = "Fredoka"


def build_theme() -> ft.Theme:
    """Tema Material claro con la identidad Kitchi."""
    scheme = ft.ColorScheme(
        primary=CORAL,
        on_primary="#FFFFFF",
        primary_container=CORAL_SUAVE,
        on_primary_container=TINTA,
        secondary=VIOLETA,
        on_secondary="#FFFFFF",
        secondary_container=LAVANDA,
        on_secondary_container=TINTA,
        tertiary=MENTA,
        surface=SUPERFICIE,
        on_surface=TINTA,
        on_surface_variant=TINTA_SUAVE,
        outline=GRIS_CALIDO,
        outline_variant=GRIS_CALIDO,
        error=ERROR,
        on_error="#FFFFFF",
    )
    return ft.Theme(
        color_scheme=scheme,
        font_family=FONT,
        use_material3=True,
    )


def register_fonts(page: ft.Page) -> None:
    page.fonts = {"Fredoka": "fonts/Fredoka-Variable.ttf"}


# --- Jerarquía tipográfica (una familia, pesos) -------------------------
def display() -> ft.TextStyle:
    return ft.TextStyle(size=30, weight=ft.FontWeight.W_700, font_family=FONT, color=TINTA)


def title() -> ft.TextStyle:
    return ft.TextStyle(size=22, weight=ft.FontWeight.W_600, font_family=FONT, color=TINTA)


def section() -> ft.TextStyle:
    return ft.TextStyle(size=18, weight=ft.FontWeight.W_600, font_family=FONT, color=TINTA)


def body() -> ft.TextStyle:
    return ft.TextStyle(size=15, weight=ft.FontWeight.W_400, font_family=FONT, color=TINTA)


def button_text() -> ft.TextStyle:
    return ft.TextStyle(size=16, weight=ft.FontWeight.W_600, font_family=FONT)


def caption() -> ft.TextStyle:
    return ft.TextStyle(size=13, weight=ft.FontWeight.W_400, font_family=FONT, color=TINTA_SUAVE)
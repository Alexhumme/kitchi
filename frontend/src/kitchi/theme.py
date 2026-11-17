"""Sistema de diseño de Kitchi Studio.

Estética "Super juguete" (referencia: Super Mario Wonder / papel plastificado):
- Bordes gruesos de tinta, muy anchos abajo y a la derecha (bevel asimétrico),
  casi invisibles arriba y a la izquierda: el canto da volumen al panel.
- Sombra dura desplazada sin desenfoque.
- Patrones propios (puntos, damero, cruces, estrellas) para llenar fondos y
  separadores; se generan una vez con `scripts/generate_ui_patterns.py`.
- Rebote elástico en los toques de los componentes primarios y háptica
  cuando el dispositivo lo soporta.
"""

from __future__ import annotations

import flet as ft

# --- Paleta "plastilina" (inspirado en Super Mario Wonder) -------------------
INK = "#211B26"          # contorno / sombras de tinta
INK_SUAVE = "#3A3342"    # tinta secundaria
CREMA = "#FFF3DF"        # fondo de la app
SUPERFICIE = "#FFFBF2"   # tarjetas (blanco cálido)
CREMA_HONDO = "#FBEBCE"  # superficie cálida secundaria
PANEL = "#FFD166"        # dorado miel (barra de herramientas + paneles)
PANEL_CLARO = "#FFE29A"  # dorado suave
GRIS_CALIDO = "#EAE6DD"  # bordes internos suaves
TINTA = INK
TINTA_SUAVE = "#6B6478"

CORAL = "#FF6B6B"        # acción principal
CORAL_HONDO = "#E45555"  # pressed de coral
CORAL_SUAVE = "#FFE3E0"  # selección con coral claro
MENTA = "#70D6C1"        # éxito
MENTA_HONDA = "#2F9E8B"  # texto éxito con contraste
EXITO = MENTA_HONDA
LIMA = "#7ED957"         # verde césped Mario (acento de éxito brillante)
AMARILLO = PANEL
VIOLETA = "#7B61FF"      # acento secundario / info
MELOCOTON = "#FFB997"    # acento cálido
ROSA = "#F7D7E8"         # detalle decorativo
LAVANDA = "#DBC6FF"      # degradados puntuales
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
        navigation_bar_theme=ft.NavigationBarTheme(
            bgcolor=INK,
            indicator_color=PANEL,
            indicator_shape=ft.RoundedRectangleBorder(radius=22),
            label_text_style=ft.TextStyle(size=11, weight=ft.FontWeight.W_800, color="#FFFFFF"),
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            height=72,
            elevation=0,
        ),
    )


def register_fonts(page: ft.Page) -> None:
    page.fonts = {"Fredoka": "fonts/Fredoka-Variable.ttf"}


# --- Estética "juguete": bevel asimétrico, esquinas, sombra -----------------
# El bevel crea volumen: casi nada de ancho arriba y a la izquierda y un canto
# grueso abajo y a la derecha como si el control fuera plástico elevado.
BORDE = 3
"""Ancho nominal del borde; los componentes usan bevel asimétrico real."""

RADIO_GRANDE = 22
"""Radio de tarjetas y diálogos."""
RADIO_MEDIO = 17
"""Radio de botones y campos."""
RADIO_PASTILLA = 999
"""Radio de chips y etiquetas."""
RADIO_ICONO = 50
"""Radio de avatares y botones de icono redondos."""

SOMBRA = ft.BoxShadow(
    spread_radius=0,
    blur_radius=0,
    offset=(0, 4),
    color=f"{INK}45",
)
"""Sombra dura desplazada para el volumen juguete."""

SOMBRA_PRESS = ft.BoxShadow(
    spread_radius=0,
    blur_radius=0,
    offset=(0, 2),
    color=f"{INK}45",
)
"""Variante para el estado pulsado."""

SOMBRA_GRANDE = ft.BoxShadow(
    spread_radius=0,
    blur_radius=0,
    offset=(0, 7),
    color=f"{INK}45",
)
"""Sombra larga para elementos elevados (barra, diálogo)."""

ANIMACION_CORTA = ft.Animation(150, ft.AnimationCurve.LINEAR)
"""Respuesta rápida para toques."""
ANIMACION_REBOTE = ft.Animation(420, ft.AnimationCurve.EASE_OUT_BACK)
"""Aparición con rebote (sobreimpulso) como si el control fuera físico."""
ANIMACION_ELASTICA = ft.Animation(600, ft.AnimationCurve.ELASTIC_OUT)
"""Desaceleración elástica para celebraciones."""


def bevel(color: str = INK, *, right: int = 4, bottom: int = 5) -> ft.Border:
    """Bevel asimétrico: 0 a la izquierda y arriba; canto grueso abajo y derecha."""
    return ft.Border(
        top=ft.BorderSide(0, color),
        left=ft.BorderSide(0, color),
        right=ft.BorderSide(right, color),
        bottom=ft.BorderSide(bottom, color),
    )


def separador(kind: str = "zigzag") -> ft.Image:
    """Separador decorativo con los motivos del catálogo generado."""
    return ft.Image(
        src=f"ui/separators/{kind}.png",
        repeat=ft.ImageRepeat.REPEAT_X,
        height=12,
        opacity=1.0,
        fit=ft.BoxFit.FILL,
    )


# --- Jerarquía tipográfica (una familia, pesos) -------------------------
def display() -> ft.TextStyle:
    return ft.TextStyle(size=30, weight=ft.FontWeight.W_800, font_family=FONT, color=INK)


def title() -> ft.TextStyle:
    return ft.TextStyle(size=22, weight=ft.FontWeight.W_700, font_family=FONT, color=INK)


def section() -> ft.TextStyle:
    return ft.TextStyle(size=18, weight=ft.FontWeight.W_700, font_family=FONT, color=INK)


def body() -> ft.TextStyle:
    return ft.TextStyle(size=15, weight=ft.FontWeight.W_400, font_family=FONT, color=INK)


def button_text() -> ft.TextStyle:
    return ft.TextStyle(size=16, weight=ft.FontWeight.W_700, font_family=FONT)


def caption() -> ft.TextStyle:
    return ft.TextStyle(size=13, weight=ft.FontWeight.W_400, font_family=FONT, color=TINTA_SUAVE)

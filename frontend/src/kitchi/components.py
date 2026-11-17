"""Componentes visuales reutilizables del sistema Kitchi Studio.

Estética "Super Mario Wonder" / plastilina:
- Borde asimétrico (0 arriba y a la izquierda; canto grueso abajo y a la derecha)
  y brillo interno arriba-izquierda como reflejo de vidrio.
- Sombra dura desplazada (sin desenfoque).
- Patrones generados (`scripts/generate_ui_patterns.py`) en tarjetas y bandas.
- Rebote elástico al pulsar componentes primarios y háptica cuando el
  dispositivo lo soporta.
"""

from __future__ import annotations

import asyncio
import logging

import flet as ft

from . import icons
from . import theme as t

logger = logging.getLogger(__name__)

_HAPTICS_ENABLED = True
_ANIMATIONS_ENABLED = True
_HAPTIC_SERVICE = None


async def _fire_haptic(pattern: str) -> None:
    try:
        global _HAPTIC_SERVICE
        if _HAPTIC_SERVICE is None:
            _HAPTIC_SERVICE = ft.HapticFeedback()
        if pattern == "error":
            await _HAPTIC_SERVICE.heavy_impact()
        elif pattern == "success":
            await _HAPTIC_SERVICE.light_impact()
        else:
            await _HAPTIC_SERVICE.light_impact()
    except Exception:  # web/desktop o cliente sin servicio: no pasa nada
        logger.debug("sin retroalimentación háptica", exc_info=True)


def haptic(pattern: str = "light") -> None:
    """Vibración breve para toques (solo móvil; sin soporte, se ignora)."""
    if not _HAPTICS_ENABLED:
        return
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(_fire_haptic(pattern))
    except RuntimeError:
        pass


def mounted(control: ft.Control) -> bool:
    """En Flet 1.x, control.page lanza excepción si no está montado."""
    try:
        _ = control.page
        return True
    except RuntimeError:
        return False


def set_animations_enabled(enabled: bool) -> None:
    global _ANIMATIONS_ENABLED
    _ANIMATIONS_ENABLED = bool(enabled)


def set_haptics_enabled(enabled: bool) -> None:
    global _HAPTICS_ENABLED
    _HAPTICS_ENABLED = bool(enabled)


def wire_tap(handler, pattern: str = "light"):
    """Envuelve un callback para que el toque vibre y rebote (esquema físico)."""

    async def _handler(e):
        haptic(pattern)
        if handler is None:
            return None
        result = handler(e)
        if asyncio.iscoroutine(result):
            return await result
        return result

    return _handler


# --- bevel / sombra helpers ---------------------------------------------------

def _bevel(color: str = t.INK, *, right: int = 4, bottom: int = 5) -> ft.Border:
    return t.bevel(color, right=right, bottom=bottom)


# --- botones primarios y secundarios -------------------------------------------

def primary_button(text: str, on_click, icon: str | None = None,
                   disabled: bool = False, expand: bool = False) -> ft.FilledButton:
    haptic_target = "light"

    async def _on_tap(e) -> None:
        haptic(haptic_target)
        await wire_tap(on_click, haptic_target)(e)

    content = ft.Row(
        [ft.Icon(icons.get(icon), size=20, color="#FFFFFF") if icon else None,
         ft.Text(text, style=t.button_text(), color="#FFFFFF")],
        spacing=9,
        alignment=ft.MainAxisAlignment.CENTER,
        tight=True,
    ) if icon else ft.Text(text, style=t.button_text(), color="#FFFFFF")
    return ft.FilledButton(
        content=content,
        on_click=_on_tap,
        disabled=disabled,
        expand=expand,
        scale=1.0,
        animate_scale=t.ANIMACION_REBOTE,
        style=ft.ButtonStyle(
            bgcolor=t.CORAL,
            color="#FFFFFF",
            overlay_color=t.CORAL_HONDO,
            side=ft.BorderSide(6, t.INK),
            padding=ft.Padding.symmetric(vertical=16, horizontal=24),
            shape=ft.RoundedRectangleBorder(radius=t.RADIO_MEDIO),
            elevation=7,
            shadow_color=t.INK,
        ),
    )


def secondary_button(text: str, on_click, icon: str | None = None,
                     disabled: bool = False) -> ft.OutlinedButton:
    haptic_target = "light"

    async def _on_tap(e) -> None:
        haptic(haptic_target)
        await wire_tap(on_click, haptic_target)(e)

    content = ft.Row(
        [ft.Icon(icons.get(icon), size=18, color=t.INK) if icon else None,
         ft.Text(text, style=t.button_text(), color=t.INK)],
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER,
        tight=True,
    ) if icon else ft.Text(text, style=t.button_text(), color=t.INK)
    return ft.OutlinedButton(
        content=content,
        on_click=_on_tap,
        disabled=disabled,
        scale=1.0,
        animate_scale=t.ANIMACION_REBOTE,
        style=ft.ButtonStyle(
            bgcolor=t.SUPERFICIE,
            color=t.INK,
            overlay_color=t.CREMA_HONDO,
            side=ft.BorderSide(4, t.INK),
            padding=ft.Padding.symmetric(vertical=13, horizontal=18),
            shape=ft.RoundedRectangleBorder(radius=t.RADIO_MEDIO),
            elevation=5,
            shadow_color=t.INK,
        ),
    )


# --- chips / avatares ---------------------------------------------------------

def chip(label: str, bgcolor: str = t.CREMA_HONDO, color: str = t.INK,
         icon: str | None = None, dense: bool = False) -> ft.Container:
    text_size = 10 if dense else 12
    content = [ft.Text(label, size=text_size, weight=ft.FontWeight.W_700, color=color)]
    if icon:
        content.insert(0, ft.Icon(icons.get(icon), size=10 if dense else 14, color=color))
    return ft.Container(
        content=ft.Row(content, spacing=4 if dense else 6, tight=True),
        padding=(
            ft.Padding.symmetric(horizontal=9, vertical=4)
            if dense
            else ft.Padding.symmetric(horizontal=12, vertical=6)
        ),
        bgcolor=bgcolor,
        border_radius=t.RADIO_PASTILLA,
        border=_bevel(t.INK, right=3, bottom=4),
        shadow=[t.SOMBRA],
        tooltip=label if icon else None,
    )


def avatar(name: str | None, size: int = 40, bgcolor: str | None = None) -> ft.Container:
    """Avatar de inicial con anillo chunky determinado por nombre."""

    initial = (name or "?").strip()[:1].upper() or "?"
    palette = (t.CORAL, t.VIOLETA, t.MENTA_HONDA, t.ADVERTENCIA, t.ERROR, t.INK)
    index = sum(ord(ch) for ch in (name or "?")) % len(palette)
    return ft.Container(
        content=ft.Text(initial, size=int(size * 0.52), weight=ft.FontWeight.W_800,
                        color="#FFFFFF"),
        width=size,
        height=size,
        bgcolor=bgcolor or palette[index],
        border_radius=size // 2,
        border=ft.Border.all(3, t.INK),
        alignment=ft.Alignment.CENTER,
        shadow=[t.SOMBRA],
    )


# --- tarjetas / paneles con patrón ---------------------------------------------

def pattern_image(name: str, repeat: ft.ImageRepeat = ft.ImageRepeat.REPEAT,
                  opacity: float = 1.0, border_radius: int = t.RADIO_GRANDE,
                  expand: bool = True) -> ft.Image:
    return ft.Image(
        src=f"ui/patterns/{name}.png",
        repeat=repeat,
        opacity=opacity,
        border_radius=border_radius,
        expand=expand,
    )


def pattern_card(content: ft.Control, padding: int | tuple = 16,
                 pattern: str = "dots_soft", pattern_opacity: float = 1.0,
                 surface_alpha: float = 0.88) -> ft.Container:
    """Panel con patrón de plastilina y superficie semitransparente encima."""
    return ft.Container(
        content=ft.Stack(
            [
                pattern_image(pattern, opacity=pattern_opacity, border_radius=t.RADIO_GRANDE),
                ft.Container(
                    content=content,
                    padding=padding,
                    border_radius=t.RADIO_GRANDE,
                    bgcolor=f"{t.SUPERFICIE}{int(surface_alpha * 255):02X}",
                    border=_bevel(t.INK, right=5, bottom=6),
                    shadow=[t.SOMBRA],
                ),
            ],
        ),
        border_radius=t.RADIO_GRANDE,
        expand=False,
    )


def card(content: ft.Control, padding: int | tuple = 16, bgcolor: str = t.SUPERFICIE,
         border_color: str = t.INK, radius: int = t.RADIO_GRANDE) -> ft.Container:
    return ft.Container(
        content=content,
        padding=padding,
        bgcolor=bgcolor,
        border_radius=radius,
        border=_bevel(t.INK, right=5, bottom=6),
        shadow=[t.SOMBRA],
    )


def divider(kind: str = "zigzag") -> ft.Row:
    """Separador decorativo grueso con motivos propios."""
    return ft.Row(
        [
            ft.Image(
                src=f"ui/separators/{kind}.png",
                repeat=ft.ImageRepeat.REPEAT_X,
                height=13,
                expand=True,
            ),
        ],
        expand=True,
    )


def flow(items: list[ft.Control], *, per_row: int = 3, spacing: int = 6,
         run_spacing: int = 6) -> ft.Column:
    """Sustituto de `ft.Row(..., wrap=True)`.

    El cliente web de Flet 1.1.2 no pinta el `Wrap` (la página queda en gris),
    así que los elementos se agrupan en filas de a lo sumo `per_row`.
    """
    rows = [ft.Row(items[start:start + per_row], spacing=spacing) for start in range(0, len(items), per_row)]
    return ft.Column(rows, spacing=run_spacing)


def section_title(text: str, subtitle: str | None = None) -> ft.Column:
    controls = [ft.Text(text, style=t.section())]
    if subtitle:
        controls.append(ft.Text(subtitle, style=t.caption()))
    return ft.Column(controls, spacing=2)


def app_bar(title: str, *, on_back=None, subtitle: str | None = None,
            right: ft.Control | None = None, tone: str = t.INK) -> ft.Control:
    """App bar de sección al estilo Mario Wonder: barra oscura con chip de regreso."""
    children = []
    if on_back is not None:
        children.append(
            ft.Container(
                content=ft.Icon(icons.get("arrow_back"), size=22, color="#FFFFFF"),
                width=40,
                height=40,
                bgcolor=tone,
                border_radius=20,
                border=t.bevel(t.INK, right=3, bottom=4),
                alignment=ft.Alignment.CENTER,
                on_click=on_back,
                tooltip="Volver",
                ink=True,
            )
        )
    children.append(
        ft.Column(
            [ft.Text(title, size=22, weight=ft.FontWeight.W_800, color="#FFFFFF")]
            + ([ft.Text(subtitle, size=12, color="#FFFFFFCC")] if subtitle else []),
            spacing=0,
            expand=True,
        )
    )
    if right is not None:
        children.append(right)
    return ft.Container(
        content=ft.Row(children, spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        bgcolor=tone,
        border=t.bevel(t.INK, right=0, bottom=5),
    )


def section_header(text: str, icon: str = "star", subtitle: str | None = None) -> ft.Row:
    """Encabezado de sección con firma física: chip de icono + texto."""
    children = [
        ft.Container(
            content=ft.Icon(icons.get(icon), size=18, color="#FFFFFF"),
            width=32,
            height=32,
            bgcolor=t.INK,
            border_radius=16,
            border=_bevel(t.INK, right=2, bottom=2),
            alignment=ft.Alignment.CENTER,
        ),
        ft.Column(
            [ft.Text(text, style=t.section())] + ([ft.Text(subtitle, style=t.caption())] if subtitle else []),
            spacing=0,
        ),
    ]
    return ft.Row(children, spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)


def banner(text: str, icon: str = "info_outline", tone: str = "info") -> ft.Container:
    tones = {
        "info": ("#E7DEF7", t.INK),
        "warning": ("#FBEBCB", t.ADVERTENCIA),
        "success": ("#D8F2E4", t.EXITO),
        "error": ("#FAD4D4", t.ERROR),
    }
    bg, fg = tones.get(tone, tones["info"])
    return ft.Container(
        content=ft.Row(
            [ft.Icon(icons.get(icon), size=18, color=fg),
             ft.Text(text, size=13, color=fg, expand=True, weight=ft.FontWeight.W_600)],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=ft.Padding.symmetric(horizontal=14, vertical=12),
        bgcolor=bg,
        border=_bevel(fg, right=3, bottom=4),
        border_radius=t.RADIO_MEDIO,
    )


def empty_state(icon: str, title: str, body: str, action: ft.Control | None = None) -> ft.Container:
    controls: list[ft.Control] = [
        ft.Container(
            content=ft.Icon(icons.get(icon), size=44, color=t.INK),
            width=96,
            height=96,
            bgcolor=t.PANEL_CLARO,
            border_radius=48,
            border=_bevel(t.INK, right=4, bottom=5),
        ),
        ft.Text(title, style=t.section(), text_align=ft.TextAlign.CENTER),
        ft.Text(body, style=t.body(), text_align=ft.TextAlign.CENTER),
    ]
    if action:
        controls.append(ft.Container(action, padding=ft.Padding.only(top=6)))
    inner = ft.Column(controls, spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    return ft.Container(
        content=ft.Stack(
            [
                ft.Image(src="ui/patterns/stars_spark.png", repeat=ft.ImageRepeat.REPEAT,
                         expand=True, opacity=0.9),
                ft.Container(
                    content=inner,
                    bgcolor="#D9FFFBF2",
                    border_radius=t.RADIO_GRANDE - 4,
                    alignment=ft.Alignment.CENTER,
                    padding=ft.Padding.symmetric(vertical=8, horizontal=8),
                ),
            ],
        ),
        padding=ft.Padding.symmetric(vertical=28, horizontal=16),
        bgcolor=t.CREMA_HONDO,
        border_radius=t.RADIO_GRANDE,
        border=_bevel(t.INK, right=4, bottom=5),
        shadow=[t.SOMBRA],
    )


def field_shell(content: ft.Control) -> ft.Control:
    """Marco chunky para campos de texto (mismo lenguaje que los botones)."""
    return ft.Container(
        content=content,
        bgcolor=t.SUPERFICIE,
        border=_bevel(t.INK, right=4, bottom=5),
        border_radius=t.RADIO_MEDIO,
        padding=ft.Padding.symmetric(horizontal=12, vertical=2),
        shadow=[t.SOMBRA],
    )


def notify(page: ft.Page, text: str, tone: str = "info") -> None:
    haptic("success" if tone == "success" else ("error" if tone == "error" else "light"))
    colors = {"info": t.INK, "success": t.EXITO, "error": t.ERROR, "warning": t.ADVERTENCIA}
    tone_icons = {"info": "info_outline", "success": "check_circle", "error": "error_outline",
                  "warning": "warning_amber"}
    page.show_dialog(
        ft.SnackBar(
            content=ft.Row(
                [ft.Icon(icons.get(tone_icons.get(tone, "info_outline")), size=18, color="#FFFFFF"),
                 ft.Text(text, size=14, weight=ft.FontWeight.W_600, color="#FFFFFF", expand=True)],
                spacing=8,
            ),
            bgcolor=colors.get(tone, t.INK),
            behavior=ft.SnackBarBehavior.FLOATING,
        )
    )


def confirm_dialog(page: ft.Page, title: str, body: str, on_confirm,
                   confirm_label: str = "Confirmar", danger: bool = False) -> None:
    def handle_confirm(e):
        haptic("error" if danger else "light")
        page.pop_dialog()
        on_confirm(e)

    page.show_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text(title, style=t.section()),
            content=ft.Text(body, style=t.body()),
            shape=ft.RoundedRectangleBorder(radius=t.RADIO_GRANDE),
            bgcolor=t.SUPERFICIE,
            actions=[
                ft.TextButton("Cancelar", tooltip="Cancelar", on_click=lambda e: page.pop_dialog()),
                primary_button(
                    confirm_label,
                    handle_confirm,
                    icon="delete_outline" if danger else "check_circle",
                ),
            ],
        )
    )

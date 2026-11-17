"""Componentes visuales reutilizables del sistema Kitchi.

Estética "juguete": bordes sólidos gruesos en tinta, esquinas redondeadas,
sombra dura desplazada (sin desenfoque) y pequeños rebotes elásticos en las
interacciones. En móvil, los toques emiten retroalimentación háptica además
del cambio visual.
"""

from __future__ import annotations

import asyncio
import logging

import flet as ft

from . import icons
from . import theme as t

logger = logging.getLogger(__name__)

_HAPTICS_ENABLED = True
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


def primary_button(text: str, on_click, icon: str | None = None,
                   disabled: bool = False, expand: bool = False) -> ft.FilledButton:
    btn_ref: dict[str, ft.FilledButton] = {}

    async def _on_tap(e) -> None:
        haptic("light")
        btn = btn_ref.get("btn")
        if btn is not None and not disabled:
            btn.scale = 0.92
            btn.update()
            await asyncio.sleep(0.08)
            btn.scale = 1.0
            btn.update()
        await wire_tap(on_click, "light")(e)

    btn = ft.FilledButton(
        content=ft.Row(
            [ft.Icon(icons.get(icon), size=20), ft.Text(text, style=t.button_text())],
            spacing=9,
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        ) if icon else ft.Text(text, style=t.button_text()),
        on_click=_on_tap,
        disabled=disabled,
        expand=expand,
        scale=1.0,
        animate_scale=t.ANIMACION_REBOTE,
        style=ft.ButtonStyle(
            bgcolor=t.CORAL,
            color="#FFFFFF",
            overlay_color=t.CORAL_HONDO,
            side=ft.BorderSide(t.BORDE, t.TINTA),
            padding=ft.Padding.symmetric(vertical=15, horizontal=22),
            shape=ft.RoundedRectangleBorder(radius=t.RADIO_MEDIO),
            elevation=6,
            shadow_color=t.TINTA,
        ),
    )
    btn_ref["btn"] = btn
    return btn


def secondary_button(text: str, on_click, icon: str | None = None,
                     disabled: bool = False) -> ft.OutlinedButton:
    btn_ref: dict[str, ft.OutlinedButton] = {}

    async def _on_tap(e) -> None:
        haptic("light")
        btn = btn_ref.get("btn")
        if btn is not None and not disabled:
            btn.scale = 0.93
            btn.update()
            await asyncio.sleep(0.08)
            btn.scale = 1.0
            btn.update()
        await wire_tap(on_click, "light")(e)

    btn = ft.OutlinedButton(
        content=ft.Row(
            [ft.Icon(icons.get(icon), size=18, color=t.TINTA),
             ft.Text(text, style=t.button_text(), color=t.TINTA)],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        ) if icon else ft.Text(text, style=t.button_text(), color=t.TINTA),
        on_click=_on_tap,
        disabled=disabled,
        scale=1.0,
        animate_scale=t.ANIMACION_REBOTE,
        style=ft.ButtonStyle(
            side=ft.BorderSide(t.BORDE, t.TINTA),
            color=t.TINTA,
            overlay_color=t.CREMA_HONDO,
            padding=ft.Padding.symmetric(vertical=13, horizontal=18),
            shape=ft.RoundedRectangleBorder(radius=t.RADIO_MEDIO),
        ),
    )
    btn_ref["btn"] = btn
    return btn


def chip(label: str, bgcolor: str = t.CREMA_HONDO, color: str = t.TINTA,
         icon: str | None = None, dense: bool = False) -> ft.Container:
    text_size = 10 if dense else 12
    content = [ft.Text(label, size=text_size, weight=ft.FontWeight.W_600, color=color)]
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
        border=ft.Border.all(2, t.TINTA),
        tooltip=label if icon else None,
    )


def avatar(name: str | None, size: int = 40, bgcolor: str | None = None) -> ft.Container:
    """Avatar de inicial con color determinista por nombre (chunky)."""

    initial = (name or "?").strip()[:1].upper() or "?"
    palette = (t.CORAL, t.VIOLETA, t.MENTA_HONDA, t.ADVERTENCIA, t.ERROR, t.TINTA)
    index = sum(ord(ch) for ch in (name or "?")) % len(palette)
    return ft.Container(
        content=ft.Text(
            initial,
            size=int(size * 0.52),
            weight=ft.FontWeight.W_700,
            color="#FFFFFF",
        ),
        width=size,
        height=size,
        bgcolor=bgcolor or palette[index],
        border_radius=size // 2,
        border=ft.Border.all(2, t.TINTA),
        alignment=ft.Alignment.CENTER,
    )


def card(content: ft.Control, padding: int | tuple = 16, bgcolor: str = t.SUPERFICIE,
         border_color: str = t.TINTA, radius: int = t.RADIO_GRANDE) -> ft.Container:
    return ft.Container(
        content=content,
        padding=padding,
        bgcolor=bgcolor,
        border_radius=radius,
        border=ft.Border.all(t.BORDE, border_color),
        shadow=[t.SOMBRA],
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


def banner(text: str, icon: str = "info_outline", tone: str = "info") -> ft.Container:
    tones = {
        "info": ("#E7DEF7", t.TINTA),
        "warning": ("#FBEBCB", t.ADVERTENCIA),
        "success": ("#D8F2E4", t.EXITO),
        "error": ("#FAD4D4", t.ERROR),
    }
    bg, fg = tones.get(tone, tones["info"])
    return ft.Container(
        content=ft.Row(
            [ft.Icon(icons.get(icon), size=18, color=fg),
             ft.Text(text, size=13, color=fg, expand=True, weight=ft.FontWeight.W_500)],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=ft.Padding.symmetric(horizontal=14, vertical=12),
        bgcolor=bg,
        border=ft.Border.all(2, fg),
        border_radius=t.RADIO_MEDIO,
    )


def empty_state(icon: str, title: str, body: str, action: ft.Control | None = None) -> ft.Container:
    controls: list[ft.Control] = [
        ft.Container(
            content=ft.Icon(icons.get(icon), size=44, color=t.TINTA_SUAVE),
            width=88,
            height=88,
            bgcolor=t.CREMA_HONDO,
            border_radius=44,
            border=ft.Border.all(t.BORDE, t.TINTA_SUAVE),
        ),
        ft.Text(title, style=t.section(), text_align=ft.TextAlign.CENTER),
        ft.Text(body, style=t.body(), text_align=ft.TextAlign.CENTER),
    ]
    if action:
        controls.append(ft.Container(action, padding=ft.Padding.only(top=6)))
    return ft.Container(
        content=ft.Column(controls, spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.symmetric(vertical=28, horizontal=16),
        alignment=ft.Alignment.CENTER,
    )


def field_shell(content: ft.Control) -> ft.Control:
    """Marco chunky para campos de texto (mismo lenguaje que los botones)."""
    return ft.Container(
        content=content,
        bgcolor=t.SUPERFICIE,
        border=ft.Border.all(t.BORDE, t.TINTA),
        border_radius=t.RADIO_MEDIO,
        padding=ft.Padding.symmetric(horizontal=12, vertical=2),
        shadow=[t.SOMBRA],
    )


def notify(page: ft.Page, text: str, tone: str = "info") -> None:
    haptic("success" if tone == "success" else ("error" if tone == "error" else "light"))
    colors = {"info": t.TINTA, "success": t.EXITO, "error": t.ERROR, "warning": t.ADVERTENCIA}
    tone_icons = {"info": "info_outline", "success": "check_circle", "error": "error_outline",
                  "warning": "warning_amber"}
    page.show_dialog(
        ft.SnackBar(
            content=ft.Row(
                [ft.Icon(icons.get(tone_icons.get(tone, "info_outline")), size=18, color="#FFFFFF"),
                 ft.Text(text, size=14, weight=ft.FontWeight.W_600, color="#FFFFFF", expand=True)],
                spacing=8,
            ),
            bgcolor=colors.get(tone, t.TINTA),
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
                ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
                primary_button(
                    confirm_label,
                    handle_confirm,
                    icon="delete_outline" if danger else "check_circle",
                ),
            ],
        )
    )

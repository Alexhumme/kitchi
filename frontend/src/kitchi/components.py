"""Componentes visuales reutilizables del sistema Kitchi."""

from __future__ import annotations

import flet as ft

from . import theme as t


def mounted(control: ft.Control) -> bool:
    """En Flet 1.x, control.page lanza excepción si no está montado."""
    try:
        _ = control.page
        return True
    except RuntimeError:
        return False


def card(content: ft.Control, padding: int | tuple = 16, bgcolor: str = t.SUPERFICIE,
         border_color: str = t.GRIS_CALIDO, radius: int = 20) -> ft.Container:
    return ft.Container(
        content=content,
        padding=padding,
        bgcolor=bgcolor,
        border_radius=radius,
        border=ft.Border.all(1, border_color),
    )


def primary_button(text: str, on_click, icon: str | None = None,
                   disabled: bool = False, expand: bool = False) -> ft.FilledButton:
    return ft.FilledButton(
        content=ft.Row(
            [ft.Icon(icon, size=20), ft.Text(text, style=t.button_text())],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        ) if icon else ft.Text(text, style=t.button_text()),
        on_click=on_click,
        disabled=disabled,
        expand=expand,
        style=ft.ButtonStyle(
            bgcolor=t.CORAL,
            color="#FFFFFF",
            overlay_color=t.CORAL_HONDO,
            padding=ft.Padding.symmetric(vertical=16, horizontal=24),
            shape=ft.RoundedRectangleBorder(radius=16),
            elevation=0,
        ),
    )


def secondary_button(text: str, on_click, icon: str | None = None,
                     disabled: bool = False) -> ft.OutlinedButton:
    return ft.OutlinedButton(
        content=ft.Row(
            [ft.Icon(icon, size=18, color=t.TINTA), ft.Text(text, style=t.button_text(), color=t.TINTA)],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        ) if icon else ft.Text(text, style=t.button_text(), color=t.TINTA),
        on_click=on_click,
        disabled=disabled,
        style=ft.ButtonStyle(
            side=ft.BorderSide(1.5, t.GRIS_CALIDO),
            padding=ft.Padding.symmetric(vertical=14, horizontal=20),
            shape=ft.RoundedRectangleBorder(radius=16),
            overlay_color=t.CREMA_HONDO,
        ),
    )


def chip(label: str, bgcolor: str = t.CREMA_HONDO, color: str = t.TINTA,
         icon: str | None = None) -> ft.Container:
    content = [ft.Text(label, size=12, weight=ft.FontWeight.W_500, color=color)]
    if icon:
        content.insert(0, ft.Icon(icon, size=14, color=color))
    return ft.Container(
        content=ft.Row(content, spacing=5, tight=True),
        padding=ft.Padding.symmetric(horizontal=10, vertical=5),
        bgcolor=bgcolor,
        border_radius=999,
    )


def section_title(text: str, subtitle: str | None = None) -> ft.Column:
    controls = [ft.Text(text, style=t.section())]
    if subtitle:
        controls.append(ft.Text(subtitle, style=t.caption()))
    return ft.Column(controls, spacing=2)


def banner(text: str, icon: str = "info_outline", tone: str = "info") -> ft.Container:
    tones = {
        "info": (t.LAVANDA, t.TINTA),
        "warning": ("#FBEBCB", t.ADVERTENCIA),
        "success": ("#DFF5F0", t.EXITO),
        "error": (t.CORAL_SUAVE, t.ERROR),
    }
    bg, fg = tones.get(tone, tones["info"])
    return ft.Container(
        content=ft.Row(
            [ft.Icon(icon, size=18, color=fg), ft.Text(text, size=13, color=fg, expand=True)],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=12,
        bgcolor=bg,
        border_radius=14,
    )


def empty_state(icon: str, title: str, body: str, action: ft.Control | None = None) -> ft.Container:
    controls: list[ft.Control] = [
        ft.Container(
            content=ft.Icon(icon, size=44, color=t.TINTA_SUAVE),
            width=88,
            height=88,
            bgcolor=t.CREMA_HONDO,
            border_radius=44,
            alignment=ft.Alignment.CENTER,
        ),
        ft.Text(title, style=t.section(), text_align=ft.TextAlign.CENTER),
        ft.Text(body, style=t.caption(), text_align=ft.TextAlign.CENTER),
    ]
    if action:
        controls.append(ft.Container(action, padding=ft.Padding.only(top=6)))
    return ft.Container(
        content=ft.Column(controls, spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.symmetric(vertical=28, horizontal=16),
        alignment=ft.Alignment.CENTER,
    )


def notify(page: ft.Page, text: str, tone: str = "info") -> None:
    colors = {"info": t.TINTA, "success": t.EXITO, "error": t.ERROR, "warning": t.ADVERTENCIA}
    icons = {"info": "info_outline", "success": "check_circle", "error": "error_outline", "warning": "warning_amber"}
    page.show_dialog(
        ft.SnackBar(
            content=ft.Row(
                [ft.Icon(icons.get(tone, "info_outline"), size=18, color="#FFFFFF"),
                 ft.Text(text, size=14, color="#FFFFFF", expand=True)],
                spacing=8,
            ),
            bgcolor=colors.get(tone, t.TINTA),
            behavior=ft.SnackBarBehavior.FLOATING,
        )
    )


def confirm_dialog(page: ft.Page, title: str, body: str, on_confirm,
                   confirm_label: str = "Confirmar", danger: bool = False) -> None:
    def handle_confirm(e):
        page.pop_dialog()
        on_confirm(e)

    page.show_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text(title, style=t.section()),
            content=ft.Text(body, style=t.body()),
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor=t.SUPERFICIE,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
                ft.FilledButton(
                    ft.Text(confirm_label, color="#FFFFFF"),
                    on_click=handle_confirm,
                    style=ft.ButtonStyle(
                        bgcolor=t.ERROR if danger else t.CORAL,
                        shape=ft.RoundedRectangleBorder(radius=12),
                    ),
                ),
            ],
        )
    )
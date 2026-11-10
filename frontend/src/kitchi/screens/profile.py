"""Perfil: identidad de invitado, datos locales y cuenta (pendiente de backend)."""

from __future__ import annotations

import flet as ft

from .. import components as c
from .. import models
from .. import theme as t


def build(app) -> ft.Control:
    identity = c.card(
        ft.Row(
            [
                ft.Container(
                    content=ft.Icon("person_outline", size=30, color=t.TINTA),
                    width=60,
                    height=60,
                    bgcolor=t.LAVANDA,
                    border_radius=30,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Column(
                    [
                        ft.Text("Invitado", style=t.section()),
                        ft.Text("Creando caos sin cuenta desde la semana 1", style=t.caption()),
                        c.chip(f"{len(app.cats)}/{models.MAX_CATS} gatos guardados", bgcolor=t.CREMA_HONDO, icon="pets"),
                    ],
                    spacing=5,
                    expand=True,
                ),
            ],
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    account = c.card(
        ft.Column(
            [
                c.section_title("Cuenta", "Registro e inicio de sesión"),
                ft.Text(
                    "Con una cuenta podrás guardar tus gatos en el servidor, publicar en "
                    "el hub y copiar creaciones de otras personas.",
                    style=t.body(),
                ),
                ft.Row(
                    [
                        c.primary_button("Registrarse", None, disabled=True),
                        c.secondary_button("Iniciar sesión", None, disabled=True),
                    ],
                    spacing=10,
                ),
                c.banner(
                    "La autenticación llega con el backend (P12). El mecanismo entre Flet y "
                    "Django aún se decide en P03; no se simulan sesiones.",
                    icon="lock_outline",
                ),
            ],
            spacing=10,
        )
    )

    data = c.card(
        ft.Column(
            [
                c.section_title("Tus datos locales", "Solo en este navegador"),
                c.banner(
                    "Si borras los datos del navegador, tus gatos de invitado se pierden. "
                    "Esto es una limitación del modo invitado, no un fallo.",
                    icon="cloud_off",
                    tone="warning",
                ),
                c.secondary_button("Vaciar datos de invitado", lambda e: app.ask_clear_local(), icon="delete_outline"),
            ],
            spacing=10,
        )
    )

    about = c.card(
        ft.Column(
            [
                c.section_title("Acerca de Kitchi", "Prototipo académico"),
                ft.Text(
                    "kitchi.studio · MVP de Programación Avanzada A1. "
                    "Interfaz Flet Web + API Django REST Framework (en construcción).",
                    style=t.caption(),
                ),
                ft.Row(
                    [
                        c.chip("Semana 2 de 4", bgcolor=t.CREMA_HONDO),
                        c.chip("Frontend v0.1.0", bgcolor=t.CREMA_HONDO),
                    ],
                    spacing=6,
                    wrap=True,
                ),
            ],
            spacing=8,
        )
    )

    return ft.Column(
        [identity, account, data, about],
        spacing=14,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
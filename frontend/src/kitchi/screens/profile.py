"""Perfil: identidad y sesión (cuenta o invitado).

La configuración, el estado de la API y Acerca de viven en la vista Configuración
(engranaje de la toolbar). Aquí queda solo lo relacionado con tu perfil.
"""

from __future__ import annotations

import flet as ft

from .. import components as c
from .. import icons
from .. import models
from .. import theme as t


def build(app) -> ft.Control:
    user = app.user
    controls: list[ft.Control] = [_identity(app, user)]

    if user:
        controls.append(_account(app, user))
    else:
        controls.append(_guest_account(app))
    return ft.Column(controls, spacing=14, scroll=ft.ScrollMode.AUTO, expand=True)


def _identity(app, user: dict | None) -> ft.Control:
    if user:
        title = user.get("username") or "Cuenta"
        subtitle = user.get("email") or "Cuenta registrada"
        role = user.get("role") or "member"
        plan = "Premium simulado" if user.get("premium") else "Plan gratuito"
        icon = "person"
        background = t.AMARILLO
    else:
        title = "Invitado"
        subtitle = "Creando caos sin cuenta en este navegador"
        role = None
        plan = None
        icon = "person_outline"
        background = t.LAVANDA

    details = [
        ft.Text(title, style=t.section()),
        ft.Text(subtitle, style=t.caption()),
        c.chip(f"{len(app.cats)}/{models.MAX_CATS} gatos guardados", bgcolor=t.CREMA_HONDO, icon="pets"),
    ]
    if role:
        details.append(c.chip(f"Rol: {role}", bgcolor=t.LAVANDA, icon="admin_panel_settings"))
    if plan:
        details.append(c.chip(plan, bgcolor=t.CORAL_SUAVE, icon="workspace_premium"))

    avatar = c.avatar(title, size=60, bgcolor=background)
    return c.card(
        ft.Row(
            [
                avatar,
                ft.Column(details, spacing=5, expand=True),
            ],
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


def _guest_account(app) -> ft.Control:
    return c.card(
        ft.Column(
            [
                c.section_title("Cuenta", "Registro e inicio de sesión"),
                ft.Text(
                    "Con una cuenta guardas tus gatos en el servidor, publicas en el hub "
                    "y copias creaciones de otras personas. Tus gatos de invitado se "
                    "migran automáticamente al entrar, si hay espacio.",
                    style=t.body(),
                ),
                ft.Row(
                    [
                        c.primary_button(
                            "Registrarse",
                            lambda e: app.open_auth("register"),
                            icon="person_add",
                        ),
                        c.secondary_button(
                            "Iniciar sesión",
                            lambda e: app.open_auth("login"),
                            icon="login",
                        ),
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        )
    )


def _account(app, user: dict) -> ft.Control:
    return c.card(
        ft.Column(
            [
                c.section_title("Sesión activa", "Token de Django + permisos RBAC"),
                ft.Text(
                    f"Sesión de {user.get('username')}. Los gatos que guardes viajan a "
                    "la API y el límite de tres se aplica en el backend.",
                    style=t.body(),
                ),
                ft.Row(
                    [
                        c.secondary_button("Actualizar datos", app.refresh, icon="refresh"),
                        c.secondary_button("Cerrar sesión", app.logout, icon="logout"),
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        )
    )

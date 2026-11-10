"""Perfil: sesión real contra la API, datos locales y estado de conexión."""

from __future__ import annotations

import flet as ft

from .. import components as c
from .. import models
from .. import theme as t


def build(app) -> ft.Control:
    user = app.user
    controls: list[ft.Control] = [_identity(app, user)]

    if user:
        controls.append(_account(app, user))
    else:
        controls.append(_guest_account(app))

    controls.append(_api_status(app))
    controls.append(_local_data(app, user))
    controls.append(_about(app))
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

    return c.card(
        ft.Row(
            [
                ft.Container(
                    content=ft.Icon(icon, size=30, color=t.TINTA),
                    width=60,
                    height=60,
                    bgcolor=background,
                    border_radius=30,
                    alignment=ft.Alignment.CENTER,
                ),
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
                    wrap=True,
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
                    wrap=True,
                ),
            ],
            spacing=10,
        )
    )


def _api_status(app) -> ft.Control:
    if app.api_online:
        tone = "success"
        icon = "cloud_done"
        text = f"API conectada en {app.api.base_url}."
    elif app.api.mode == "local":
        tone = "warning"
        icon = "cloud_off"
        text = (
            "Sin API configurada: la app funciona con el catálogo empaquetado y el "
            "almacenamiento local. Define API_BASE_URL en el .env para conectar."
        )
    else:
        tone = "error"
        icon = "cloud_off"
        detail = app.api_error or "No se pudo contactar el servidor."
        text = f"API no disponible en {app.api.base_url}. {detail}"

    catalog_text = (
        "Catálogo servido por /api/catalog/."
        if app.catalog_source == "api"
        else "Se usa el catálogo provisional del cliente; ejecuta scripts/seed_catalog.py para sembrar la API."
    )
    return c.card(
        ft.Column(
            [
                c.section_title("Conexión", "Estado real, sin datos simulados"),
                c.banner(text, icon=icon, tone=tone),
                c.banner(catalog_text, icon="inventory_2", tone="info" if app.catalog_source == "api" else "warning"),
            ],
            spacing=10,
        )
    )


def _local_data(app, user: dict | None) -> ft.Control:
    if user:
        body = ft.Column(
            [
                c.section_title("Tus datos", "En el servidor"),
                ft.Text(
                    "Los gatos de esta cuenta viven en la base de datos del backend. "
                    "El almacenamiento del navegador solo conserva el token de sesión.",
                    style=t.body(),
                ),
            ],
            spacing=8,
        )
    else:
        body = ft.Column(
            [
                c.section_title("Tus datos locales", "Solo en este navegador"),
                c.banner(
                    "Si borras los datos del navegador, tus gatos de invitado se pierden. "
                    "Esto es una limitación del modo invitado, no un fallo.",
                    icon="cloud_off",
                    tone="warning",
                ),
                c.secondary_button(
                    "Vaciar datos de invitado",
                    lambda e: app.ask_clear_local(),
                    icon="delete_outline",
                ),
            ],
            spacing=10,
        )
    return c.card(body)


def _about(app) -> ft.Control:
    mode = "API HTTP" if app.api.mode == "http" else "modo local"
    return c.card(
        ft.Column(
            [
                c.section_title("Acerca de Kitchi", "Prototipo académico"),
                ft.Text(
                    "kitchi.studio · MVP de Programación Avanzada A1. "
                    "Interfaz Flet Web + API Django REST Framework.",
                    style=t.caption(),
                ),
                ft.Row(
                    [
                        c.chip("Semana 2 de 4", bgcolor=t.CREMA_HONDO),
                        c.chip("Frontend v0.2.0", bgcolor=t.CREMA_HONDO),
                        c.chip(mode, bgcolor=t.CREMA_HONDO, icon="cable"),
                    ],
                    spacing=6,
                    wrap=True,
                ),
            ],
            spacing=8,
        )
    )

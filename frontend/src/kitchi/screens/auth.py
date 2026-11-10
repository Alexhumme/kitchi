"""Inicio de sesión y registro contra la API (token de Django, ADR-005)."""

from __future__ import annotations

import flet as ft

from .. import components as c
from .. import theme as t


def build(app, mode: str) -> ft.Control:
    return AuthScreen(app, mode).build()


class AuthScreen:
    def __init__(self, app, mode: str):
        self.app = app
        self.mode = mode if mode in ("login", "register") else "login"
        self.error = ft.Text("", size=13, color=t.ERROR, visible=False)
        self.submit_button = ft.FilledButton()
        self.username = ft.TextField(
            label="Nombre de usuario",
            autofocus=True,
            border_radius=14,
            bgcolor=t.SUPERFICIE,
            border_color=t.GRIS_CALIDO,
            focused_border_color=t.CORAL,
        )
        self.email = ft.TextField(
            label="Correo electrónico",
            keyboard_type=ft.KeyboardType.EMAIL,
            border_radius=14,
            bgcolor=t.SUPERFICIE,
            border_color=t.GRIS_CALIDO,
            focused_border_color=t.CORAL,
            visible=self.mode == "register",
        )
        self.password = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            border_radius=14,
            bgcolor=t.SUPERFICIE,
            border_color=t.GRIS_CALIDO,
            focused_border_color=t.CORAL,
        )
        self.confirm = ft.TextField(
            label="Repite la contraseña",
            password=True,
            can_reveal_password=True,
            border_radius=14,
            bgcolor=t.SUPERFICIE,
            border_color=t.GRIS_CALIDO,
            focused_border_color=t.CORAL,
            visible=self.mode == "register",
        )
        self.password.on_submit = self._submit

    def build(self) -> ft.Control:
        is_login = self.mode == "login"
        title = "Iniciar sesión" if is_login else "Crear cuenta"
        subtitle = (
            "Entra para guardar tus gatos en el servidor y publicar en el hub."
            if is_login
            else "Tu cuenta guarda hasta 3 gatos y te permite publicar en el hub."
        )
        self.submit_button = c.primary_button(
            "Entrar" if is_login else "Crear mi cuenta",
            self._submit,
            icon="login" if is_login else "person_add",
            expand=True,
        )

        fields: list[ft.Control] = [self.username, self.email, self.password, self.confirm]
        if not is_login:
            fields.append(
                c.banner(
                    "La contraseña debe tener al menos 8 caracteres y no ser demasiado común.",
                    icon="shield_outlined",
                )
            )

        switch_label = "¿No tienes cuenta? Regístrate" if is_login else "¿Ya tienes cuenta? Inicia sesión"
        switch_mode = "register" if is_login else "login"

        body: list[ft.Control] = [
            ft.Row(
                [
                    ft.IconButton(
                        "arrow_back",
                        tooltip="Volver",
                        icon_color=t.TINTA,
                        on_click=lambda e: self.app.close_auth(),
                    ),
                    ft.Column(
                        [
                            ft.Text(title, style=t.title()),
                            ft.Text(subtitle, style=t.caption()),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                spacing=6,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ]

        if not self.app.api_online:
            body.append(
                c.banner(
                    "La API no está disponible ahora mismo. Arranca el backend o revisa "
                    "API_BASE_URL en el .env; el modo invitado sigue funcionando.",
                    icon="cloud_off",
                    tone="warning",
                )
            )

        body.extend(
            [
                c.card(ft.Column(fields, spacing=12), padding=16),
                self.error,
                self.submit_button,
                ft.TextButton(
                    switch_label,
                    on_click=lambda e: self.app.open_auth(switch_mode),
                ),
            ]
        )
        return ft.Column(body, spacing=14, scroll=ft.ScrollMode.AUTO, expand=True)

    async def _submit(self, _event) -> None:
        if not self.submit_button.disabled:
            self._set_busy(True)
            self._show_error("", visible=False)
            username = (self.username.value or "").strip()
            password = self.password.value or ""
            email = (self.email.value or "").strip()
            confirm = self.confirm.value or ""

            error = self._validate(username, password, email, confirm)
            if error:
                self._show_error(error)
                self._set_busy(False)
                return

            message = await self.app.authenticate(self.mode, username, password, email)
            if message:
                self._show_error(message)
                self._set_busy(False)

    def _validate(self, username: str, password: str, email: str, confirm: str) -> str | None:
        if not username:
            return "Escribe tu nombre de usuario."
        if not password:
            return "Escribe tu contraseña."
        if self.mode == "register":
            if not email or "@" not in email:
                return "Escribe un correo electrónico válido."
            if len(password) < 8:
                return "La contraseña debe tener al menos 8 caracteres."
            if password != confirm:
                return "Las contraseñas no coinciden."
        return None

    def _show_error(self, message: str, visible: bool = True) -> None:
        self.error.value = message
        self.error.visible = visible and bool(message)
        if c.mounted(self.error):
            self.error.update()

    def _set_busy(self, busy: bool) -> None:
        self.submit_button.disabled = busy
        self.submit_button.content = ft.Text(
            "Conectando…" if busy else ("Entrar" if self.mode == "login" else "Crear mi cuenta")
        )
        if c.mounted(self.submit_button):
            self.submit_button.update()

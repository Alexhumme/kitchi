"""Mis gatos: colección local del invitado con abrir, editar y eliminar."""

from __future__ import annotations

import flet as ft

from .. import catalog
from .. import components as c
from .. import models
from .. import theme as t


def build(app) -> ft.Control:
    cats = app.cats
    account = app.user is not None
    header = ft.Row(
        [
            c.section_title(
                "Mis gatos",
                f"Cuenta de {app.user.get('username')}" if account else "Tu colección en este dispositivo",
            ),
            c.chip(f"{len(cats)}/{models.MAX_CATS}", bgcolor=t.CORAL_SUAVE, icon="pets"),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    controls: list[ft.Control] = [header]
    if account:
        controls.append(
            c.banner(
                "Tus gatos están guardados en la API. El límite de tres se valida en el backend.",
                icon="cloud_done",
                tone="success",
            )
        )
        if not app.api_online:
            controls.append(
                c.banner(
                    app.api_error or "La API no está disponible; no se pueden modificar tus gatos ahora.",
                    icon="cloud_off",
                    tone="warning",
                )
            )
    else:
        controls.append(
            c.banner(
                "Modo invitado: tus gatos viven en este navegador. Si borras sus datos, "
                "se pierden. Regístrate para guardarlos en tu cuenta.",
                icon="cloud_off",
                tone="warning",
            )
        )

    if not cats:
        controls.append(
            c.card(
                c.empty_state(
                    "pets",
                    "Aún no hay gatos por aquí",
                    "Crea tu primer gato: elige piezas, combina sin miedo y guárdalo.",
                    c.primary_button("Crear mi primer gato", lambda e: app.open_editor(None), icon="add"),
                )
            )
        )
    else:
        for cat in sorted(cats, key=lambda x: x["updated_at"], reverse=True):
            controls.append(_cat_card(app, cat))
        if len(cats) < models.MAX_CATS:
            controls.append(c.secondary_button("Crear otro gato", lambda e: app.open_editor(None), icon="add"))
        else:
            controls.append(
                c.banner("Llegaste al límite de 3 gatos del modo invitado. Elimina uno para crear otro.",
                         icon="info_outline")
            )

    return ft.Column(controls, spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)


def _cat_card(app, cat: dict) -> ft.Control:
    summary = catalog.config_summary(cat["configuration"])
    updated = cat["updated_at"][:10]
    return c.card(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon("pets", size=24, color=t.CORAL),
                            width=44,
                            height=44,
                            bgcolor=t.CORAL_SUAVE,
                            border_radius=22,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Column(
                            [
                                ft.Text(cat["name"], size=16, weight=ft.FontWeight.W_600, color=t.TINTA),
                                ft.Text(f"Actualizado: {updated}", style=t.caption()),
                            ],
                            spacing=1,
                            expand=True,
                        ),
                        ft.IconButton("edit", tooltip="Editar", icon_color=t.TINTA,
                                      on_click=lambda e, cid=cat["id"]: app.edit_cat(cid)),
                        ft.IconButton("delete_outline", tooltip="Eliminar", icon_color=t.ERROR,
                                      on_click=lambda e, cid=cat["id"]: app.ask_delete_cat(cid)),
                    ],
                    spacing=6,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [c.chip(f"{label}: {name}", bgcolor=t.CREMA_HONDO) for label, name in summary],
                    spacing=6,
                    wrap=True,
                    run_spacing=6,
                ),
            ],
            spacing=10,
        ),
        padding=14,
    )
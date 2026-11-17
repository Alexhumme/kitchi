"""Mis gatos: colección con abrir, editar, eliminar y publicar (P18)."""

from __future__ import annotations

import flet as ft

from .. import catalog
from .. import cat_view
from .. import components as c
from .. import icons
from .. import models
from .. import theme as t
from ..api import ApiError


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

    def share_widget():
        if not app.user:
            return ft.IconButton(
                icons.get("share"),
                tooltip="Crea una cuenta o inicia sesión para publicar",
                icon_color=t.TINTA_SUAVE,
                on_click=lambda e: app.open_auth("login"),
            )
        if str(cat.get("id")) in app.published_cat_ids:
            return c.chip("Publicado", icon="check_circle", dense=True, bgcolor=t.MENTA, color=t.TINTA)
        return ft.IconButton(
            icons.get("share"),
            tooltip="Publicar en el hub",
            icon_color=t.TINTA,
            on_click=lambda e: _open_publish_dialog(app, cat),
        )

    return c.card(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(icons.get("pets"), size=24, color=t.CORAL),
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
                        ft.IconButton(icons.get("edit"), tooltip="Editar", icon_color=t.TINTA,
                                      on_click=lambda e, cid=cat["id"]: app.edit_cat(cid)),
                        share_widget(),
                        ft.IconButton(icons.get("delete_outline"), tooltip="Eliminar", icon_color=t.ERROR,
                                      on_click=lambda e, cid=cat["id"]: app.ask_delete_cat(cid)),
                    ],
                    spacing=6,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(
                    "  ·  ".join(f"{label}: {name}" for label, name in summary),
                    style=t.caption(),
                ),
            ],
            spacing=10,
        ),
        padding=14,
    )

def _open_publish_dialog(app, cat: dict) -> None:
    """Diálogo para publicar un gato propio en el hub (P18)."""
    page = app.page

    title_field = ft.TextField(
        label="Título",
        value=cat.get("name") or "",
        max_length=120,
        autofocus=True,
        filled=True,
        bgcolor=t.SUPERFICIE,
        border=ft.OutlineInputBorder(
            border_radius=t.RADIO_MEDIO,
            side=ft.BorderSide(t.BORDE, t.TINTA),
        ),
    )
    description_field = ft.TextField(
        label="Descripción",
        hint_text="Cuenta un poquito de tu gato…",
        max_length=500,
        min_lines=2,
        max_lines=4,
        filled=True,
        bgcolor=t.SUPERFICIE,
        border=ft.OutlineInputBorder(
            border_radius=t.RADIO_MEDIO,
            side=ft.BorderSide(t.BORDE, t.TINTA),
        ),
    )
    visibility_toggle = ft.Switch(
        label="Pública — cualquier persona puede verla",
        value=True,
        active_color=t.CORAL,
    )

    async def do_publish(_event) -> None:
        title = (title_field.value or "").strip()
        if not title:
            c.notify(page, "Ponle un título a la publicación.", "error")
            return
        visibility = "public" if visibility_toggle.value else "private"
        description = (description_field.value or "").strip()
        page.pop_dialog()
        try:
            import asyncio

            await asyncio.to_thread(
                app.api.publish_cat, cat["id"], title, description, visibility
            )
        except ApiError as exc:
            if getattr(exc, "code", "") == "PUBLICATION_ALREADY_EXISTS":
                app.published_cat_ids.add(str(cat.get("id")))
                c.notify(page, "Este gato ya está publicado en el hub.", "info")
            else:
                c.notify(page, exc.user_message(), "error")
            app.rebuild_current()
            return
        app.published_cat_ids.add(str(cat.get("id")))
        c.notify(page, f"«{title}» publicada en el hub.", "success")
        await app.refresh_feed(append=False)
        app.rebuild_current()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Publicar en el hub", style=t.section()),
        bgcolor=t.SUPERFICIE,
        shape=ft.RoundedRectangleBorder(radius=t.RADIO_GRANDE),
        content=ft.Column(
            [
                ft.Row(
                    [
                        cat_view.cat_face(cat.get("configuration") or {}, 96),
                        ft.Column(
                            [
                                ft.Text(
                                    cat.get("name") or "Sin nombre",
                                    weight=ft.FontWeight.W_700,
                                    color=t.TINTA,
                                ),
                                ft.Text(
                                    "Así se verá en las tarjetas del feed.",
                                    style=t.caption(),
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                title_field,
                description_field,
                visibility_toggle,
            ],
            tight=True,
            spacing=10,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
            c.primary_button("Publicar", do_publish, icon="share"),
        ],
    )
    page.show_dialog(dialog)


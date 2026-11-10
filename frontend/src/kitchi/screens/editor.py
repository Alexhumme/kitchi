"""Editor de creación: el gato al centro, categorías a los lados.

La barra inferior global NO se sustituye: vive a nivel de page. Los controles
laterales solo modifican el personaje. La previsualización usa placeholders de
color del catálogo hasta que lleguen los assets de la diseñadora (P06); el
editor ya es funcional y honesto: selección, deshacer, reiniciar, azar, guardado
y render provisional en tiempo real.
"""

from __future__ import annotations

import flet as ft

from .. import catalog
from .. import components as c
from .. import models
from .. import theme as t
from ..editor_state import EditorState

LEFT_KEYS = ("fur", "eyes", "hair")
RIGHT_KEYS = ("top", "bottom", "accessory")


class EditorScreen:
    def __init__(self, app, state: EditorState | None = None):
        self.app = app
        self.state = state or EditorState()
        self._status_chip = ft.Container()
        self._undo_button = ft.Container()
        self._options_panel = ft.Column(spacing=8)
        self._combo_panel = ft.Container()
        self._stage_host = ft.Container()
        self._title = ft.Text(style=t.title())

    # --- construcción ---------------------------------------------------
    def build(self) -> ft.Control:
        self._title.value = "Editar gato" if self.state.cat_id else "Estudio de creación"
        toolbar = ft.Row(
            [
                ft.Column(
                    [self._title, ft.Text("Elige una categoría y prueba piezas", style=t.caption()),
                     self._status_chip],
                    spacing=3,
                    expand=True,
                ),
                self._undo_button,
                ft.IconButton("restart_alt", tooltip="Reiniciar combinación", icon_color=t.TINTA_SUAVE,
                              on_click=self._on_reset),
                ft.IconButton("casino", tooltip="Combinación al azar", icon_color=t.TINTA_SUAVE,
                              on_click=self._on_random),
                ft.IconButton("add", tooltip="Empezar un gato nuevo", icon_color=t.TINTA_SUAVE,
                              on_click=self._on_new),
            ],
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        stage_row = ft.Row(
            [
                self._side_controls(LEFT_KEYS),
                ft.Container(self._stage(), expand=True),
                self._side_controls(RIGHT_KEYS),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        save_bar = ft.Column(
            [
                c.primary_button(
                    "Guardar gato" if not self.state.cat_id else "Guardar cambios",
                    self._on_save,
                    icon="save_outlined",
                    expand=True,
                ),
                ft.Text(
                    f"Se guarda en tu cuenta ({self.app.user.get('username')}, máximo 3 gatos)."
                    if self.app.user
                    else "Modo invitado: se guarda en este navegador (máximo 3 gatos).",
                    style=t.caption(),
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=6,
        )

        self._refresh()
        return ft.Column(
            [
                toolbar,
                stage_row,
                c.card(self._options_panel, padding=14),
                self._combo_panel,
                save_bar,
            ],
            spacing=14,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _side_controls(self, keys: tuple[str, ...]) -> ft.Column:
        buttons = []
        for key in keys:
            cat = catalog.get_category(key)
            selected = self.state.selected_category == key
            buttons.append(
                ft.Container(
                    key=key,
                    content=ft.Stack(
                        [
                            ft.Column(
                                [
                                    ft.Icon(cat.icon, size=22, color=t.CORAL if selected else t.TINTA_SUAVE),
                                    ft.Text(
                                        cat.short_label,
                                        size=11,
                                        weight=ft.FontWeight.W_600 if selected else ft.FontWeight.W_500,
                                        color=t.TINTA,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                ],
                                spacing=3,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Container(
                                content=ft.Icon("check_circle", size=14, color=t.CORAL),
                                right=2,
                                top=2,
                                visible=selected,
                            ),
                        ],
                    ),
                    width=74,
                    height=72,
                    bgcolor=t.CORAL_SUAVE if selected else t.SUPERFICIE,
                    border=ft.Border.all(2 if selected else 1, t.CORAL if selected else t.GRIS_CALIDO),
                    border_radius=18,
                    alignment=ft.Alignment.CENTER,
                    on_click=lambda e, k=key: self._on_category(k),
                    ink=True,
                )
            )
        return ft.Column(buttons, spacing=8)

    def _stage(self) -> ft.Control:
        self._stage_host.height = 300
        self._stage_host.bgcolor = t.CREMA_HONDO
        self._stage_host.border = ft.Border.all(1, t.GRIS_CALIDO)
        self._stage_host.border_radius = 24
        self._stage_host.padding = 12
        self._stage_host.alignment = ft.Alignment.CENTER
        return self._stage_host

    def _selected(self, key: str):
        return catalog.get_option(key, self.state.configuration.get(key, ""))

    def _render_stage(self) -> ft.Control:
        """Previsualización provisional con los colores del catálogo.

        No usa imágenes: cada pieza se representa con su color y etiqueta para
        que el editor demuestre el cambio en tiempo real. Cuando la diseñadora
        entregue los assets (P06/P08) esta capa se sustituirá por el render real.
        """
        fur = self._selected("fur")
        eyes = self._selected("eyes")
        hair = self._selected("hair")
        top = self._selected("top")
        bottom = self._selected("bottom")
        accessory = self._selected("accessory")
        if not all((fur, eyes, hair, top, bottom, accessory)):
            return ft.Text("Configuración incompleta", style=t.caption())

        eye_width = 22 if eyes.code == "round_green" else (26 if eyes.code == "big_blue" else 28)
        eye_height = 22 if eyes.code != "almond_amber" else 15

        def eye() -> ft.Container:
            return ft.Container(
                content=ft.Container(
                    width=eye_width * 0.42,
                    height=eye_width * 0.42,
                    bgcolor=t.TINTA,
                    border_radius=eye_width,
                ),
                width=eye_width,
                height=eye_height,
                bgcolor=eyes.swatch,
                border=ft.Border.all(2, t.TINTA),
                border_radius=eye_width,
                alignment=ft.Alignment.CENTER,
            )

        ears = [
            ft.Container(width=52, height=52, bgcolor=fur.swatch,
                         border=ft.Border.all(3, t.TINTA), border_radius=18, left=32, top=16),
            ft.Container(width=52, height=52, bgcolor=fur.swatch,
                         border=ft.Border.all(3, t.TINTA), border_radius=18, right=32, top=16),
        ]
        face = ft.Stack(
            [
                *ears,
                ft.Container(
                    width=178, height=154, bgcolor=fur.swatch,
                    border=ft.Border.all(3, t.TINTA), border_radius=82, left=26, top=34,
                ),
                ft.Container(
                    width=128, height=36, bgcolor=hair.swatch,
                    border=ft.Border.all(2, t.TINTA), border_radius=18, left=51, top=41,
                ),
                ft.Container(
                    content=ft.Row([eye(), eye()], spacing=26, alignment=ft.MainAxisAlignment.CENTER),
                    width=104, left=63, top=106,
                ),
                ft.Container(
                    width=12, height=8, bgcolor=t.CORAL, border_radius=6, left=109, top=150,
                ),
                ft.Container(
                    width=44, height=3, bgcolor=t.TINTA, border_radius=2, left=93, top=166,
                ),
                self._accessory_layer(accessory),
            ],
            width=230,
            height=210,
        )

        def piece(label: str, option) -> ft.Container:
            return ft.Container(
                content=ft.Row(
                    [
                        ft.Container(width=14, height=14, bgcolor=option.swatch,
                                     border=ft.Border.all(1, t.TINTA), border_radius=7),
                        ft.Text(f"{label}: {option.name}", size=11, color=t.TINTA),
                    ],
                    spacing=5,
                    tight=True,
                ),
                padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                bgcolor=t.SUPERFICIE,
                border=ft.Border.all(1, t.GRIS_CALIDO),
                border_radius=999,
            )

        return ft.Column(
            [
                c.chip("Vista previa con placeholders", bgcolor=t.SUPERFICIE, icon="brush"),
                face,
                ft.Row(
                    [piece("Sup.", top), piece("Inf.", bottom), piece("Extra", accessory)],
                    spacing=5,
                    wrap=True,
                    run_spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(
                    "Sin assets finales: los colores representan cada pieza del catálogo.",
                    size=11,
                    color=t.TINTA_SUAVE,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def _accessory_layer(self, accessory) -> ft.Control:
        if accessory.code == "glasses":
            lens = ft.Container(
                width=34, height=30, border=ft.Border.all(3, t.TINTA), border_radius=10
            )
            return ft.Container(
                content=ft.Row(
                    [lens, ft.Container(width=12, height=3, bgcolor=t.TINTA), lens],
                    spacing=0,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=104,
                left=63,
                top=100,
            )
        if accessory.code == "bow":
            return ft.Container(
                content=ft.Icon("star", size=30, color=accessory.swatch),
                left=158,
                top=20,
            )
        return ft.Container(
            width=132, height=40, bgcolor=accessory.swatch,
            border=ft.Border.all(2, t.TINTA), border_radius=20, left=49, top=18,
        )

    # --- partes dinámicas ------------------------------------------------
    def _refresh(self) -> None:
        self._status_chip.content = c.chip(
            "Cambios sin guardar" if self.state.dirty else ("Guardado" if self.state.cat_id else "Gato nuevo"),
            bgcolor=t.AMARILLO if self.state.dirty else t.CREMA_HONDO,
            icon="fiber_manual_record" if self.state.dirty else "check_circle",
        )
        self._undo_button.content = ft.IconButton(
            "undo",
            tooltip="Deshacer",
            icon_color=t.TINTA if self.state.history else t.GRIS_CALIDO,
            disabled=not self.state.history,
            on_click=self._on_undo,
        )
        self._options_panel.controls = self._option_rows()
        self._stage_host.content = self._render_stage()
        self._combo_panel.content = c.card(
            ft.Column(
                [
                    c.section_title("Tu combinación", "Se actualiza al instante con cada elección"),
                    ft.Row(
                        [
                            c.chip(f"{label}: {name}", bgcolor=t.CREMA_HONDO)
                            for label, name in catalog.config_summary(self.state.configuration)
                        ],
                        spacing=6,
                        wrap=True,
                        run_spacing=6,
                    ),
                ],
                spacing=8,
            ),
            padding=14,
        )

    def _option_rows(self) -> list[ft.Control]:
        cat = catalog.get_category(self.state.selected_category)
        rows: list[ft.Control] = [
            ft.Row(
                [
                    ft.Icon(cat.icon, size=18, color=t.CORAL),
                    ft.Text(cat.label, size=15, weight=ft.FontWeight.W_600, color=t.TINTA),
                    ft.Text(cat.tagline, style=t.caption(), expand=True, text_align=ft.TextAlign.RIGHT),
                ],
                spacing=8,
            )
        ]
        current = self.state.configuration.get(cat.key)
        for opt in cat.options:
            selected = opt.code == current
            rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                width=34,
                                height=34,
                                bgcolor=opt.swatch,
                                border=ft.Border.all(2, t.TINTA if selected else t.GRIS_CALIDO),
                                border_radius=17,
                            ),
                            ft.Column(
                                [
                                    ft.Text(opt.name, size=14, weight=ft.FontWeight.W_600, color=t.TINTA),
                                    ft.Text(opt.description, style=t.caption()),
                                ],
                                spacing=1,
                                expand=True,
                            ),
                            ft.Icon("check_circle" if selected else "radio_button_unchecked",
                                    size=22, color=t.CORAL if selected else t.GRIS_CALIDO),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=12,
                    bgcolor=t.CORAL_SUAVE if selected else t.SUPERFICIE,
                    border=ft.Border.all(2 if selected else 1, t.CORAL if selected else t.GRIS_CALIDO),
                    border_radius=16,
                    on_click=lambda e, k=cat.key, code=opt.code: self._on_option(k, code),
                    ink=True,
                )
            )
        return rows

    def _update_dynamic(self) -> None:
        self._refresh()
        for control in (self._status_chip, self._undo_button, self._options_panel, self._combo_panel):
            if c.mounted(control):
                control.update()

    # --- eventos ---------------------------------------------------------
    def _on_category(self, key: str) -> None:
        self.state.selected_category = key
        self._rebuild_stage_controls()

    def _rebuild_stage_controls(self) -> None:
        # Los botones laterales reflejan la categoría activa: reconstruir la pantalla
        # completa es la vía simple y estable en Flet.
        self.app.rebuild_current()

    def _on_option(self, key: str, code: str) -> None:
        if self.state.select_option(key, code):
            self._update_dynamic()

    def _on_undo(self, e) -> None:
        if self.state.undo():
            self._update_dynamic()

    def _on_reset(self, e) -> None:
        if self.state.reset():
            self._update_dynamic()
            c.notify(self.app.page, "Combinación reiniciada", "info")

    def _on_random(self, e) -> None:
        self.state.randomize()
        self._update_dynamic()
        c.notify(self.app.page, "¡Caos aleatorio generado!", "success")

    def _on_new(self, e) -> None:
        def start_fresh(_):
            self.app.open_editor(None)

        if self.state.dirty:
            c.confirm_dialog(
                self.app.page,
                "¿Empezar de cero?",
                "Tienes cambios sin guardar que se perderán.",
                start_fresh,
                confirm_label="Empezar de cero",
            )
        else:
            start_fresh(e)

    def _on_save(self, e) -> None:
        page = self.app.page
        name_field = ft.TextField(
            label="Nombre de tu gato",
            value=self.state.cat_name,
            autofocus=True,
            border_radius=14,
            bgcolor=t.SUPERFICIE,
            border_color=t.GRIS_CALIDO,
            focused_border_color=t.CORAL,
        )

        async def do_save(_):
            name = name_field.value or ""
            error = models.validate_name(name)
            if error:
                c.notify(page, error, "error")
                return
            page.pop_dialog()
            await self.app.save_cat(name.strip(), self.state)
            self._title.value = "Editar gato"
            self._update_dynamic()
            if c.mounted(self._title):
                self._title.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Guardar gato", style=t.section()),
            content=ft.Column(
                [
                    name_field,
                    ft.Text("Un nombre digno de su caos.", style=t.caption()),
                ],
                spacing=8,
                tight=True,
            ),
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor=t.SUPERFICIE,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
                c.primary_button("Guardar", do_save, icon="save_outlined"),
            ],
        )
        name_field.on_submit = do_save
        page.show_dialog(dialog)
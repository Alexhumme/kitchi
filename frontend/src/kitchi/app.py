"""Shell de Kitchi Studio: cabecera, contenido y navegación inferior global.

La barra inferior mantiene las cinco secciones en todas las pantallas,
incluido el editor (directriz UI/UX). El estado del editor es independiente
del estado de navegación.
"""

from __future__ import annotations

import flet as ft

from . import catalog
from . import components as c
from . import models
from . import storage
from . import theme as t
from .api import ApiClient
from .editor_state import EditorState
from .screens import editor as editor_screen
from .screens import hub, my_cats, profile, stickers

SECTIONS = (
    ("Navegar", "explore_outlined"),
    ("Mis gatos", "pets"),
    ("Crear", "add_circle"),
    ("Stickers IA", "auto_awesome"),
    ("Perfil", "person_outline"),
)


class KitchiApp:
    def __init__(self, page: ft.Page, guest_storage=None, api: ApiClient | None = None):
        self.page = page
        self.storage = guest_storage or storage.MemoryStorage()
        self.api = api or ApiClient()
        self.cats: list[dict] = []
        self.section = 0
        self._editor: editor_screen.EditorScreen | None = None
        self._content = ft.Column(expand=True, spacing=0)
        self._nav: ft.NavigationBar | None = None

    async def start(self) -> None:
        page = self.page
        t.register_fonts(page)
        page.title = "kitchi.studio — caos adorable, a tu manera"
        page.bgcolor = t.CREMA
        page.theme = t.build_theme()
        page.padding = 0
        page.spacing = 0

        self.cats = await storage.load_cats(self.storage)

        header = ft.Container(
            content=ft.Row(
                [
                    ft.Icon("pets", size=24, color=t.CORAL),
                    ft.Text("kitchi.studio", size=20, weight=ft.FontWeight.W_700, color=t.TINTA),
                    ft.Container(expand=True),
                    c.chip("Invitado", bgcolor=t.CREMA_HONDO, icon="person_outline"),
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            bgcolor=t.CREMA,
            border=ft.Border(bottom=ft.BorderSide(1, t.GRIS_CALIDO)),
        )

        body = ft.Container(
            content=self._content,
            expand=True,
            padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        )

        self._nav = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=icon_name, label=label)
                for label, icon_name in SECTIONS
            ],
            selected_index=0,
            on_change=self._on_nav_change,
            bgcolor=t.SUPERFICIE,
            indicator_color=t.CORAL_SUAVE,
            height=68,
        )

        page.add(ft.Column([header, body], spacing=0, expand=True))
        page.navigation_bar = self._nav
        self.go(0)
        page.update()

    # --- navegación ------------------------------------------------------
    def _on_nav_change(self, e) -> None:
        self.go(int(e.control.selected_index))

    def go(self, index: int) -> None:
        self.section = index
        if self._nav is not None and self._nav.selected_index != index:
            self._nav.selected_index = index
        self.rebuild_current()

    def rebuild_current(self) -> None:
        if self.section == 0:
            screen = hub.build(self)
        elif self.section == 1:
            screen = my_cats.build(self)
        elif self.section == 2:
            if self._editor is None:
                self._editor = editor_screen.EditorScreen(self)
            screen = self._editor.build()
        elif self.section == 3:
            screen = stickers.build(self)
        else:
            screen = profile.build(self)
        self._content.controls = [screen]
        if self._nav is not None and c.mounted(self._nav):
            self._nav.update()
        if c.mounted(self._content):
            self._content.update()

    def open_editor(self, cat: dict | None) -> None:
        state = EditorState(configuration=cat["configuration"], cat=cat) if cat else EditorState()
        self._editor = editor_screen.EditorScreen(self, state)
        self.go(2)

    def edit_cat(self, cat_id: str) -> None:
        cat = next((x for x in self.cats if x["id"] == cat_id), None)
        if cat:
            self.open_editor(cat)

    # --- mutaciones de gatos (modo invitado) ------------------------------
    async def save_cat(self, name: str, state: EditorState) -> dict | None:
        if not models.can_add_cat(self.cats, state.cat_id):
            c.notify(self.page, "Ya tienes 3 gatos. Elimina uno para guardar otro.", "error")
            return None
        config_errors = catalog.validate_config(state.configuration)
        if config_errors:
            c.notify(self.page, "La combinación no es válida.", "error")
            return None

        existing = next((x for x in self.cats if x["id"] == state.cat_id), None) if state.cat_id else None
        if existing:
            existing["name"] = name
            existing["configuration"] = state.to_payload()
            existing["updated_at"] = models.now_iso()
            cat = existing
        else:
            cat = models.new_cat(name, state.to_payload())
            self.cats.append(cat)

        await storage.persist_cats(self.storage, self.cats)
        state.mark_saved(cat["id"], name)
        c.notify(self.page, f"'{name}' guardado en este navegador.", "success")
        return cat

    def ask_delete_cat(self, cat_id: str) -> None:
        cat = next((x for x in self.cats if x["id"] == cat_id), None)
        if not cat:
            return

        async def do_delete(_):
            self.cats = [x for x in self.cats if x["id"] != cat_id]
            await storage.persist_cats(self.storage, self.cats)
            if self._editor and self._editor.state.cat_id == cat_id:
                self._editor = None
            self.rebuild_current()
            self._notify_with_undo(f"'{cat['name']}' eliminado.", cat)

        c.confirm_dialog(
            self.page,
            "¿Eliminar este gato?",
            f"'{cat['name']}' se borrará de este navegador. Podrás deshacerlo justo después.",
            do_delete,
            confirm_label="Eliminar",
            danger=True,
        )

    def _notify_with_undo(self, text: str, deleted_cat: dict) -> None:
        async def restore(_):
            if models.can_add_cat(self.cats):
                self.cats.append(deleted_cat)
                await storage.persist_cats(self.storage, self.cats)
                self.rebuild_current()
                c.notify(self.page, f"'{deleted_cat['name']}' restaurado.", "success")

        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(text, size=14, color="#FFFFFF"),
                bgcolor=t.TINTA,
                behavior=ft.SnackBarBehavior.FLOATING,
                action=ft.SnackBarAction(label="Deshacer", text_color=t.AMARILLO, on_click=restore),
            )
        )

    def ask_clear_local(self) -> None:
        async def do_clear(_):
            self.cats = []
            self._editor = None
            await storage.persist_cats(self.storage, self.cats)
            self.rebuild_current()
            c.notify(self.page, "Datos de invitado vaciados.", "info")

        c.confirm_dialog(
            self.page,
            "¿Vaciar los datos locales?",
            "Se eliminarán todos los gatos guardados en este navegador. No se puede deshacer.",
            do_clear,
            confirm_label="Vaciar todo",
            danger=True,
        )


async def main(page: ft.Page) -> None:
    prefs = ft.SharedPreferences()
    app = KitchiApp(page, storage.FletPrefsStorage(prefs))
    await app.start()
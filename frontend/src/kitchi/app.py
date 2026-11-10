"""Shell de Kitchi Studio: sesión, cabecera, contenido y navegación inferior.

La barra inferior mantiene las cinco secciones en todas las pantallas. El
estado de sesión decide si los gatos viven en la API (cuenta) o en el
almacenamiento del navegador (invitado); el editor es el mismo en ambos casos.
"""

from __future__ import annotations

import asyncio

import flet as ft

from . import catalog
from . import components as c
from . import models
from . import storage
from . import theme as t
from .api import ApiClient, ApiError
from .editor_state import EditorState
from .screens import auth as auth_screen
from .screens import editor as editor_screen
from .screens import hub, my_cats, profile, stickers

SECTIONS = (
    ("Navegar", "explore_outlined"),
    ("Mis gatos", "pets"),
    ("Crear", "add_circle"),
    ("Stickers IA", "auto_awesome"),
    ("Perfil", "person_outline"),
)

BUNDLED_POSES = [
    {"code": code, "name": name}
    for code, name in (
        ("greeting", "Saludo"),
        ("happy", "Alegría"),
        ("angry", "Enfado"),
        ("sad", "Tristeza"),
        ("surprised", "Sorpresa"),
        ("sleepy", "Sueño"),
    )
]


class KitchiApp:
    def __init__(self, page: ft.Page, guest_storage=None, api: ApiClient | None = None):
        self.page = page
        self.storage = guest_storage or storage.MemoryStorage()
        self.api = api or ApiClient()
        self.token: str | None = None
        self.user: dict | None = None
        self.cats: list[dict] = []
        self.poses: list[dict] = list(BUNDLED_POSES)
        self.publications: list[dict] = []
        self.publications_error: str | None = None
        self.api_online = False
        self.api_error: str | None = None
        self.catalog_source = catalog.CATALOG_SOURCE
        self.auth_mode: str | None = None
        self.section = 0
        self._editor: editor_screen.EditorScreen | None = None
        self._content = ft.Column(expand=True, spacing=0)
        self._nav: ft.NavigationBar | None = None
        self._identity_host = ft.Container()

    # --- arranque --------------------------------------------------------
    async def start(self) -> None:
        page = self.page
        t.register_fonts(page)
        page.title = "kitchi.studio — caos adorable, a tu manera"
        page.bgcolor = t.CREMA
        page.theme = t.build_theme()
        page.padding = 0
        page.spacing = 0

        await self._bootstrap()

        header = ft.Container(
            content=ft.Row(
                [
                    ft.Icon("pets", size=24, color=t.CORAL),
                    ft.Text("kitchi.studio", size=20, weight=ft.FontWeight.W_700, color=t.TINTA),
                    ft.Container(expand=True),
                    self._identity_host,
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            bgcolor=t.CREMA,
            border=ft.Border(bottom=ft.BorderSide(1, t.GRIS_CALIDO)),
        )
        self._render_identity()

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

    async def _bootstrap(self) -> None:
        self.token, self.user = await storage.load_session(self.storage)
        if self.token:
            self.api.set_token(self.token)
            try:
                self.user = await asyncio.to_thread(self.api.me)
            except ApiError as exc:
                self.token = None
                self.user = None
                self.api.set_token(None)
                await storage.clear_session(self.storage)
                self.api_error = exc.user_message()
        await self._load_backend_catalog()
        await self._load_cats()
        await self._load_publications()

    async def _load_backend_catalog(self) -> None:
        if self.api.mode != "http":
            self.api_online = False
            self.catalog_source = "bundled"
            return
        try:
            payload = await asyncio.to_thread(self.api.get_catalog)
        except ApiError as exc:
            self.api_online = False
            self.api_error = exc.user_message()
        else:
            self.api_online = True
            self.api_error = None
            self.catalog_source = "api" if catalog.apply_api_catalog(payload) else "bundled"
        try:
            poses = await asyncio.to_thread(self.api.get_poses)
        except ApiError:
            poses = []
        self.poses = poses or list(BUNDLED_POSES)

    async def _load_cats(self) -> None:
        if not self.user:
            self.cats = await storage.load_cats(self.storage)
            return
        try:
            records = await asyncio.to_thread(self.api.list_cats)
        except ApiError as exc:
            self.cats = []
            self.api_error = exc.user_message()
            return
        self.cats = [models.cat_from_api(record) for record in records]

    async def _load_publications(self) -> None:
        self.publications = []
        self.publications_error = None
        if not self.api_online:
            return
        try:
            data = await asyncio.to_thread(self.api.get_publications)
        except ApiError as exc:
            self.publications_error = (
                exc.user_message() if exc.status != 404 else "El endpoint /api/publications/ aún no existe (P18)."
            )
            return
        results = data.get("results", data) if isinstance(data, dict) else data
        self.publications = results if isinstance(results, list) else []

    async def refresh(self, _event=None) -> None:
        await self._load_backend_catalog()
        await self._load_cats()
        await self._load_publications()
        self.rebuild_current()
        c.notify(self.page, "Datos de la API actualizados.", "success")

    # --- navegación ------------------------------------------------------
    def _on_nav_change(self, e) -> None:
        self.go(int(e.control.selected_index))

    def go(self, index: int) -> None:
        self.section = index
        self.auth_mode = None
        if self._nav is not None and self._nav.selected_index != index:
            self._nav.selected_index = index
        self.rebuild_current()

    def open_auth(self, mode: str) -> None:
        self.auth_mode = mode
        self.rebuild_current()

    def close_auth(self) -> None:
        self.auth_mode = None
        self.rebuild_current()

    def rebuild_current(self) -> None:
        if self.auth_mode:
            screen = auth_screen.build(self, self.auth_mode)
        elif self.section == 0:
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

    def _render_identity(self) -> None:
        if self.user:
            label = self.user.get("username") or "Cuenta"
            chip = c.chip(label, bgcolor=t.AMARILLO, icon="person")
        else:
            chip = c.chip("Invitado", bgcolor=t.CREMA_HONDO, icon="person_outline")
        self._identity_host.content = chip
        if c.mounted(self._identity_host):
            self._identity_host.update()

    def open_editor(self, cat: dict | None) -> None:
        configuration = catalog.normalize_configuration(cat.get("configuration")) if cat else None
        state = EditorState(configuration=configuration, cat=cat) if cat else EditorState()
        self._editor = editor_screen.EditorScreen(self, state)
        self.go(2)

    def edit_cat(self, cat_id) -> None:
        cat = next((x for x in self.cats if str(x["id"]) == str(cat_id)), None)
        if cat:
            self.open_editor(cat)

    # --- sesión ----------------------------------------------------------
    async def authenticate(self, mode: str, username: str, password: str, email: str = "") -> str | None:
        guest_cats = list(self.cats) if not self.user else []
        try:
            if mode == "register":
                data = await asyncio.to_thread(self.api.register, username, email, password)
            else:
                data = await asyncio.to_thread(self.api.login, username, password)
        except ApiError as exc:
            return exc.user_message()

        token = data.get("token") if isinstance(data, dict) else None
        if not token:
            return "La API no devolvió un token de sesión."
        self.token = token
        self.user = data.get("user") or {"username": username}
        self.api.set_token(token)
        await storage.persist_session(self.storage, token, self.user)
        self.api_online = True
        self.api_error = None
        await self._load_cats()
        await self._load_publications()
        self.auth_mode = None
        self._render_identity()
        if guest_cats:
            await self._migrate_guest_cats(guest_cats)
        self.go(1)
        c.notify(self.page, f"Sesión iniciada como {self.user.get('username')}.", "success")
        return None

    async def _migrate_guest_cats(self, guest_cats: list[dict]) -> None:
        migrated_ids: set[str] = set()
        for cat in guest_cats:
            if len(self.cats) >= models.MAX_CATS:
                break
            try:
                record = await asyncio.to_thread(self.api.create_cat, cat["name"], cat["configuration"])
            except ApiError:
                continue
            self.cats.append(models.cat_from_api(record))
            migrated_ids.add(str(cat["id"]))
        if not migrated_ids:
            return
        local_cats = await storage.load_cats(self.storage)
        await storage.persist_cats(
            self.storage, [cat for cat in local_cats if str(cat["id"]) not in migrated_ids]
        )
        c.notify(self.page, f"{len(migrated_ids)} gato(s) de invitado pasaron a tu cuenta.", "success")

    async def logout(self, _event=None) -> None:
        try:
            await asyncio.to_thread(self.api.logout)
        except ApiError:
            pass
        self.token = None
        self.user = None
        self.api.set_token(None)
        await storage.clear_session(self.storage)
        await self._load_cats()
        self.auth_mode = None
        self._render_identity()
        self.go(0)
        c.notify(self.page, "Sesión cerrada. Vuelves al modo invitado.", "info")

    # --- mutaciones de gatos ----------------------------------------------
    async def save_cat(self, name: str, state: EditorState) -> dict | None:
        config_errors = catalog.validate_config(state.configuration)
        if config_errors:
            c.notify(self.page, "La combinación no es válida para el catálogo actual.", "error")
            return None

        if self.user:
            return await self._save_cat_api(name, state)

        if not models.can_add_cat(self.cats, state.cat_id):
            c.notify(self.page, "Ya tienes 3 gatos. Elimina uno para guardar otro.", "error")
            return None

        existing = next((x for x in self.cats if str(x["id"]) == str(state.cat_id)), None) if state.cat_id else None
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

    async def _save_cat_api(self, name: str, state: EditorState) -> dict | None:
        try:
            if state.cat_id:
                record = await asyncio.to_thread(
                    self.api.update_cat, state.cat_id, name, state.to_payload()
                )
            else:
                record = await asyncio.to_thread(self.api.create_cat, name, state.to_payload())
        except ApiError as exc:
            c.notify(self.page, exc.user_message(), "error")
            return None

        cat = models.cat_from_api(record)
        index = next(
            (i for i, current in enumerate(self.cats) if str(current["id"]) == str(cat["id"])), None
        )
        if index is None:
            self.cats.append(cat)
        else:
            self.cats[index] = cat
        state.mark_saved(cat["id"], cat["name"])
        c.notify(self.page, f"'{cat['name']}' guardado en tu cuenta.", "success")
        return cat

    def ask_delete_cat(self, cat_id) -> None:
        cat = next((x for x in self.cats if str(x["id"]) == str(cat_id)), None)
        if not cat:
            return

        if self.user:
            async def do_delete_api(_):
                try:
                    await asyncio.to_thread(self.api.delete_cat, cat_id)
                except ApiError as exc:
                    c.notify(self.page, exc.user_message(), "error")
                    return
                self.cats = [x for x in self.cats if str(x["id"]) != str(cat_id)]
                if self._editor and str(self._editor.state.cat_id) == str(cat_id):
                    self._editor = None
                self.rebuild_current()
                c.notify(self.page, f"'{cat['name']}' eliminado de tu cuenta.", "info")

            c.confirm_dialog(
                self.page,
                "¿Eliminar este gato?",
                f"'{cat['name']}' se borrará de tu cuenta en el servidor.",
                do_delete_api,
                confirm_label="Eliminar",
                danger=True,
            )
            return

        async def do_delete(_):
            self.cats = [x for x in self.cats if str(x["id"]) != str(cat_id)]
            await storage.persist_cats(self.storage, self.cats)
            if self._editor and str(self._editor.state.cat_id) == str(cat_id):
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

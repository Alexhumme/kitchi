"""Shell de Kitchi Studio: sesión, cabecera, contenido y navegación inferior.

La barra inferior mantiene las cinco secciones en todas las pantallas. El
estado de sesión decide si los gatos viven en la API (cuenta) o en el
almacenamiento del navegador (invitado); el editor es el mismo en ambos casos.
"""

from __future__ import annotations

import asyncio
import logging

import flet as ft

from . import catalog
from . import components as c
from . import icons
from . import models
from . import storage
from . import theme as t
from .api import ApiClient, ApiError
from .editor_state import EditorState
from .screens import auth as auth_screen
from .screens import editor as editor_screen
from .screens import hub, my_cats, profile, settings as settings_screen, stickers
from .screens import public_profile as public_profile_screen

logger = logging.getLogger(__name__)

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
    def __init__(
        self,
        page: ft.Page,
        guest_storage=None,
        api: ApiClient | None = None,
        storage_factory=None,
    ):
        self.page = page
        self.storage = guest_storage or storage.MemoryStorage()
        self.storage_factory = storage_factory
        self.storage_notice: str | None = None
        self.api = api or ApiClient()
        self.token: str | None = None
        self.user: dict | None = None
        self.cats: list[dict] = []
        self.poses: list[dict] = list(BUNDLED_POSES)
        self.publications: list[dict] = []
        self.feed_page: int = 1
        self.feed_total: int = 0
        self.feed_query: str = ""
        self.feed_has_more: bool = False
        self.feed_searching: bool = False
        self.feed_error: str | None = None
        self.published_cat_ids: set[str] = set()
        self.api_online = False
        self.api_error: str | None = None
        self.catalog_source = catalog.CATALOG_SOURCE
        self.auth_mode: str | None = None
        self.section = 0
        self.show_settings = False
        self.public_profile: str | None = None
        self._search_field: ft.TextField | None = None
        self.sound_enabled = True
        self.animations_enabled = True
        self.haptic_enabled = True
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

        header = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icons.get("pets"), size=26, color=t.CORAL),
                    ft.Text("kitchi.studio", size=20, weight=ft.FontWeight.W_700, color=t.TINTA),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icons.get("settings"),
                        tooltip="Configuración de la app",
                        icon_color=t.TINTA,
                        on_click=lambda e: self.toggle_settings(),
                    ),
                    self._identity_host,
                ],
                spacing=6,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            bgcolor=t.CREMA,
            border=ft.Border(bottom=ft.BorderSide(t.BORDE, t.TINTA)),
        )
        self._render_identity()

        body = ft.Container(
            content=self._content,
            expand=True,
            padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        )

        self._nav = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=icons.get(icon_name), label=label)
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
        # El armazón se pinta antes de tocar el almacenamiento: si el navegador
        # no responde, la app sigue siendo usable en modo invitado en memoria.
        page.update()
        self.go(0)
        page.update()

        await self._attach_storage()
        try:
            await self._bootstrap()
        except Exception:  # noqa: BLE001 - la pantalla debe quedar usable igual
            logger.exception("Fallo al cargar el estado inicial")
            c.notify(self.page, "No se pudieron cargar los datos iniciales.", "error")
        self.rebuild_current()
        self._render_identity()
        page.update()

    async def _attach_storage(self) -> None:
        """Conecta el almacenamiento del navegador ya con la página pintada."""
        if self.storage_factory is None:
            return
        try:
            store = await self.storage_factory()
        except Exception:  # noqa: BLE001 - nunca debe tumbar el arranque
            logger.exception("Fallo al abrir el almacenamiento del navegador")
            store = None
        if store is None:
            self.storage = storage.MemoryStorage()
            self.storage_notice = (
                "No se pudo abrir el almacenamiento de este navegador. "
                "Los gatos de invitado no se guardarán en esta sesión."
            )
            logger.warning("Almacenamiento del navegador no disponible; se usa memoria")
            return
        self.storage = store
        self.storage_notice = None

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
        await self._load_settings()
        await self._load_backend_catalog()
        await self._load_cats()
        await self.refresh_feed(append=False)
        await self._load_own_publications()

    async def _load_settings(self) -> None:
        """Preferencias de la experiencia: sonido, animaciones y vibración."""
        try:
            sound_raw = await self.storage.get("kitchi.ui.sound")
            anim_raw = await self.storage.get("kitchi.ui.animations")
            haptic_raw = await self.storage.get("kitchi.ui.haptic")
            self.sound_enabled = (sound_raw or "on") != "off"
            self.animations_enabled = (anim_raw or "on") != "off"
            self.haptic_enabled = (haptic_raw or "on") != "off"
            c.set_haptics_enabled(self.haptic_enabled)
        except Exception:  # noqa: BLE001 - preferencias no deben tumbar el arranque
            logger.warning("sin preferencias de UI; se usan valores activados", exc_info=True)

    async def set_sound_enabled(self, enabled: bool) -> None:
        self.sound_enabled = enabled
        await self._persist_setting("kitchi.ui.sound", "on" if enabled else "off")

    async def set_animations_enabled(self, enabled: bool) -> None:
        self.animations_enabled = enabled
        await self._persist_setting("kitchi.ui.animations", "on" if enabled else "off")

    async def set_haptic_enabled(self, enabled: bool) -> None:
        self.haptic_enabled = enabled
        c.set_haptics_enabled(enabled)
        await self._persist_setting("kitchi.ui.haptic", "on" if enabled else "off")

    async def _persist_setting(self, key: str, value: str) -> None:
        try:
            await self.storage.set(key, value)
        except Exception:  # noqa: BLE001
            logger.warning("no se pudo guardar la preferencia %s", key, exc_info=True)

    async def _load_own_publications(self) -> None:
        """Mapa gato → publicado para la pantalla de Mis gatos (P18)."""
        self.published_cat_ids = set()
        if not self.user or self.api.mode != "http":
            return
        try:
            payload = await asyncio.to_thread(
                self.api.get_publications, 1, 50, None, self.user.get("username")
            )
        except ApiError as exc:
            logger.info("no se pudieron listar las publicaciones propias: %s", exc)
            return
        results = payload.get("results", payload) if isinstance(payload, dict) else payload
        if isinstance(results, list):
            for item in results:
                cat = item.get("cat") or {}
                cid = cat.get("id")
                if cid is not None:
                    self.published_cat_ids.add(str(cid))

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

    async def refresh_feed(self, append: bool = False) -> None:
        """Carga el feed público del hub (P18), reemplazando o añadiendo al final."""
        if self.api.mode != "http":
            self.publications = []
            self.feed_has_more = False
            self.feed_searching = False
            self.feed_error = None
            return
        page = self.feed_page + 1 if append else 1
        try:
            data = await asyncio.to_thread(
                self.api.get_publications, page, 12, self.feed_query or None, None
            )
        except ApiError as exc:
            self.feed_error = (
                exc.user_message()
                if exc.status not in (404, 401)
                else "El hub de publicaciones no está disponible en este momento."
            )
            self.feed_searching = False
            return
        results = data.get("results", data) if isinstance(data, dict) else data
        results = results if isinstance(results, list) else []
        if append:
            self.publications.extend(results)
            self.feed_page = page
        else:
            self.publications = results
            self.feed_page = page
        self.feed_total = (
            int(data.get("count", len(self.publications))) if isinstance(data, dict) else len(self.publications)
        )
        self.feed_has_more = bool(data.get("next")) if isinstance(data, dict) else False
        self.feed_searching = False
        self.feed_error = None

    async def load_more_feed(self, _event=None) -> None:
        if not self.feed_has_more:
            return
        self.feed_searching = True
        await self.refresh_feed(append=True)
        self.rebuild_current()

    async def refresh(self, _event=None) -> None:
        await self._load_backend_catalog()
        await self._load_cats()
        await self.refresh_feed(append=False)
        await self._load_own_publications()
        self.rebuild_current()
        c.notify(self.page, "Datos de la API actualizados.", "success")

    # --- navegación ------------------------------------------------------
    def _on_nav_change(self, e) -> None:
        c.haptic("light")
        self.go(int(e.control.selected_index))

    def go(self, index: int) -> None:
        self.section = index
        self.auth_mode = None
        self.show_settings = False
        self.public_profile = None
        if self._nav is not None and self._nav.selected_index != index:
            self._nav.selected_index = index
        self.rebuild_current()

    def toggle_settings(self) -> None:
        self.show_settings = not self.show_settings
        self.public_profile = None
        self.rebuild_current()

    def close_settings(self) -> None:
        self.show_settings = False
        self.rebuild_current()

    def open_public_profile(self, username: str) -> None:
        self.public_profile = username
        self.show_settings = False
        self.rebuild_current()

    def close_public_profile(self) -> None:
        self.public_profile = None
        self.rebuild_current()

    def open_auth(self, mode: str) -> None:
        self.auth_mode = mode
        self.rebuild_current()

    def close_auth(self) -> None:
        self.auth_mode = None
        self.rebuild_current()

    def rebuild_current(self) -> None:
        if self.show_settings:
            screen = settings_screen.build(self)
        elif self.public_profile:
            screen = public_profile_screen.build(self, self.public_profile)
        elif self.auth_mode:
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
        self._content.controls = (
            [self._storage_banner()] if self.storage_notice else []
        ) + [screen]
        if self._nav is not None and c.mounted(self._nav):
            self._nav.update()
        if c.mounted(self._content):
            self._content.update()

    def _storage_banner(self) -> ft.Control:
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icons.get("warning_amber"), size=18, color=t.ADVERTENCIA),
                    ft.Text(self.storage_notice or "", size=13, color=t.TINTA, expand=True),
                ],
                spacing=8,
            ),
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            bgcolor=t.AMARILLO,
            border_radius=12,
            margin=ft.Margin.only(bottom=12),
        )

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
        await self.refresh_feed(append=False)
        await self._load_own_publications()
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
    app = KitchiApp(page, storage_factory=storage.open_browser_storage)
    await app.start()

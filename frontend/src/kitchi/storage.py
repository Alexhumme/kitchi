"""Persistencia local del modo invitado.

Los gatos de invitado viven en el almacenamiento del navegador; se advierte
al usuario que pueden perderse al borrar los datos (requisito, docs/02).
Esto no es un mecanismo de seguridad: el límite real de usuarios registrados
lo aplica el backend.
"""

from __future__ import annotations

import copy
import json

from .models import validate_cat_record

STORAGE_KEY = "kitchi.guest.cats.v1"
SESSION_KEY = "kitchi.session.v1"


class MemoryStorage:
    """Implementación en memoria para pruebas y respaldo."""

    def __init__(self):
        self._data: dict[str, str] = {}

    async def get(self, key: str) -> str | None:
        return self._data.get(key)

    async def set(self, key: str, value: str) -> None:
        self._data[key] = value


class FletPrefsStorage:
    """Adaptador sobre ft.SharedPreferences (async en Flet 1.x)."""

    def __init__(self, prefs):
        self._prefs = prefs

    async def get(self, key: str) -> str | None:
        return await self._prefs.get(key)

    async def set(self, key: str, value: str) -> None:
        await self._prefs.set(key, value)


async def load_cats(storage) -> list[dict]:
    raw = await storage.get(STORAGE_KEY)
    if not raw:
        return []
    try:
        records = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return []
    if not isinstance(records, list):
        return []
    return [r for r in records if not validate_cat_record(r)]


async def persist_cats(storage, cats: list[dict]) -> None:
    await storage.set(STORAGE_KEY, json.dumps(cats, ensure_ascii=False))


async def load_session(storage) -> tuple[str | None, dict | None]:
    raw = await storage.get(SESSION_KEY)
    if not raw:
        return None, None
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None, None
    if not isinstance(data, dict):
        return None, None
    token = data.get("token")
    user = data.get("user")
    if not isinstance(token, str) or not token:
        return None, None
    return token, user if isinstance(user, dict) else None


async def persist_session(storage, token: str, user: dict | None) -> None:
    payload = {"token": token, "user": user or {}}
    await storage.set(SESSION_KEY, json.dumps(payload, ensure_ascii=False))


async def clear_session(storage) -> None:
    await storage.set(SESSION_KEY, "")


def clone_cats(cats: list[dict]) -> list[dict]:
    return copy.deepcopy(cats)
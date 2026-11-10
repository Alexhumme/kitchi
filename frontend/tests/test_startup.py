"""Arranque tolerante a fallos del almacenamiento del navegador.

Flet 1.1.x puede no enlazar el servicio `SharedPreferences` en el cliente
(servicio registrado pero sin listener). El arranque debe reintentar con una
instancia nueva y, si no hay forma, dejar la app usable en memoria.
"""

import asyncio
import types

import flet as ft

from kitchi import storage
from kitchi.app import KitchiApp


def test_probe_returns_false_when_client_never_answers(monkeypatch):
    class SilentPrefs:
        async def get(self, key):
            await asyncio.sleep(5)

    adapter = storage.FletPrefsStorage(SilentPrefs())
    assert asyncio.run(adapter.probe(timeout=0.02)) is False


def test_probe_returns_true_on_fast_answer():
    class FastPrefs:
        async def get(self, key):
            return None

    adapter = storage.FletPrefsStorage(FastPrefs())
    assert asyncio.run(adapter.probe(timeout=0.5)) is True


async def test_open_browser_storage_uses_first_working_instance(monkeypatch):
    created = []

    class WorkingPrefs:
        def __init__(self):
            self.keys = []
            created.append(self)

        async def get(self, key):
            self.keys.append(key)
            return None

    monkeypatch.setattr(ft, "SharedPreferences", WorkingPrefs)
    store = await storage.open_browser_storage(delays=(0.0, 0.0), timeout=0.2)

    assert isinstance(store, storage.FletPrefsStorage)
    assert len(created) == 1
    assert created[0].keys == [storage.PROBE_KEY]


async def test_open_browser_storage_retries_with_new_instance(monkeypatch):
    created = []

    class FlakyPrefs:
        def __init__(self):
            self.broken = not created  # la primera instancia nunca responde
            created.append(self)

        async def get(self, key):
            if self.broken:
                await asyncio.sleep(5)
            return None

    monkeypatch.setattr(ft, "SharedPreferences", FlakyPrefs)
    store = await storage.open_browser_storage(delays=(0.0, 0.0, 0.0), timeout=0.02)

    assert store is not None
    assert len(created) == 2


async def test_open_browser_storage_gives_up_after_all_attempts(monkeypatch):
    created = []

    class BrokenPrefs:
        def __init__(self):
            created.append(self)

        async def get(self, key):
            await asyncio.sleep(5)

    monkeypatch.setattr(ft, "SharedPreferences", BrokenPrefs)
    store = await storage.open_browser_storage(delays=(0.0, 0.0), timeout=0.02)

    assert store is None
    assert len(created) == 2


async def test_attach_storage_falls_back_to_memory_and_warns():
    async def unavailable():
        return None

    app = KitchiApp(types.SimpleNamespace(), storage_factory=unavailable)
    await app._attach_storage()

    assert isinstance(app.storage, storage.MemoryStorage)
    assert app.storage_notice and "almacenamiento" in app.storage_notice


async def test_attach_storage_survives_factory_error():
    async def boom():
        raise RuntimeError("servicio roto")

    app = KitchiApp(types.SimpleNamespace(), storage_factory=boom)
    await app._attach_storage()

    assert isinstance(app.storage, storage.MemoryStorage)
    assert app.storage_notice is not None


async def test_attach_storage_keeps_working_adapter():
    class Store:
        async def get(self, key):
            return None

        async def set(self, key, value):
            pass

    store = Store()

    async def factory():
        return store

    app = KitchiApp(types.SimpleNamespace(), storage_factory=factory)
    await app._attach_storage()

    assert app.storage is store
    assert app.storage_notice is None

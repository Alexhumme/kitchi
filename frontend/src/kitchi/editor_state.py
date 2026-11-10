"""Estado del editor: configuración, historial de deshacer y suciedad.

Lógica pura y testeable, sin dependencia de Flet.
"""

from __future__ import annotations

import copy
import random

from . import catalog

MAX_HISTORY = 60


class EditorState:
    def __init__(self, configuration: dict | None = None, cat: dict | None = None):
        base = configuration if configuration is not None else catalog.default_config()
        self.configuration = copy.deepcopy(base)
        self.cat_id: str | None = cat["id"] if cat else None
        self.cat_name: str = cat["name"] if cat else ""
        self.history: list[dict] = []
        self.dirty = False
        self.selected_category: str = catalog.CATEGORY_KEYS[0]

    def _push_history(self) -> None:
        self.history.append(copy.deepcopy(self.configuration))
        if len(self.history) > MAX_HISTORY:
            self.history.pop(0)

    def select_option(self, category_key: str, code: str) -> bool:
        if not catalog.is_valid_option(category_key, code):
            return False
        if self.configuration.get(category_key) == code:
            return False
        self._push_history()
        self.configuration[category_key] = code
        self.dirty = True
        return True

    def undo(self) -> bool:
        if not self.history:
            return False
        self.configuration = self.history.pop()
        self.dirty = True
        return True

    def reset(self) -> bool:
        if self.configuration == catalog.default_config():
            return False
        self._push_history()
        self.configuration = catalog.default_config()
        self.dirty = True
        return True

    def randomize(self) -> bool:
        self._push_history()
        for cat in catalog.CATEGORIES:
            self.configuration[cat.key] = random.choice(cat.options).code
        self.dirty = True
        return True

    def mark_saved(self, cat_id: str, name: str) -> None:
        self.cat_id = cat_id
        self.cat_name = name
        self.dirty = False

    def to_payload(self) -> dict:
        return copy.deepcopy(self.configuration)
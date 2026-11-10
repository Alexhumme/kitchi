"""Modelos de datos del cliente (espejo de los contratos, no autoridad)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from . import catalog

MAX_CATS = 3
MAX_NAME_LENGTH = 40


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_cat(name: str, configuration: dict) -> dict:
    timestamp = now_iso()
    return {
        "id": uuid.uuid4().hex[:12],
        "name": name.strip(),
        "configuration": dict(configuration),
        "created_at": timestamp,
        "updated_at": timestamp,
    }


def cat_from_api(record: dict) -> dict:
    """Adapta un gato de la API al formato que usa la interfaz."""
    return {
        "id": record.get("id"),
        "name": record.get("name") or "Sin nombre",
        "configuration": catalog.normalize_configuration(record.get("configuration")),
        "created_at": record.get("created_at") or now_iso(),
        "updated_at": record.get("updated_at") or now_iso(),
    }


def validate_name(name: str) -> str | None:
    cleaned = name.strip()
    if not cleaned:
        return "Ponle un nombre a tu gato."
    if len(cleaned) > MAX_NAME_LENGTH:
        return f"Máximo {MAX_NAME_LENGTH} caracteres."
    return None


def can_add_cat(cats: list[dict], editing_id: str | None = None) -> bool:
    """Límite local de invitado; en usuarios registrados lo aplica el backend."""
    if editing_id and any(c["id"] == editing_id for c in cats):
        return True
    return len(cats) < MAX_CATS


def validate_cat_record(record: dict) -> list[str]:
    errors = []
    if not isinstance(record, dict):
        return ["Registro de gato inválido."]
    for field in ("id", "name", "created_at", "updated_at"):
        if not record.get(field):
            errors.append(f"Campo requerido ausente: {field}")
    errors.extend(catalog.validate_config(record.get("configuration", {})))
    return errors
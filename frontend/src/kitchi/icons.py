"""Resolución de nombres de iconos al tipo que exige Flet 1.x.

En Flet 1.x los iconos son ``IconData`` (``ft.Icons.PETS``), no cadenas: si se
pasa ``"pets"`` el cliente recibe un tipo no válido, la construcción de la
página falla en silencio y solo se ve el fondo (pantalla gris). Los datos del
catálogo, las poses y las tablas de tonos siguen guardando nombres legibles y
se convierten aquí, en el borde de la interfaz.
"""

from __future__ import annotations

import logging

import flet as ft

logger = logging.getLogger(__name__)

FALLBACK = ft.Icons.HELP_OUTLINE

_cache: dict[str, ft.IconData] = {}


def get(name) -> ft.IconData:
    """Devuelve el ``IconData`` de un nombre Material (``"pets"``)."""
    if isinstance(name, ft.IconData):
        return name
    key = str(name or "").strip().upper()
    cached = _cache.get(key)
    if cached is not None:
        return cached
    icon = getattr(ft.Icons, key, None)
    if icon is None:
        logger.warning("Icono desconocido %r; se usa el icono de reserva", name)
        icon = FALLBACK
    _cache[key] = icon
    return icon

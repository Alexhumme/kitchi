"""Catálogo provisional del editor.

Fuente conceptual: docs/02_REQUIREMENTS.md (6 campos × 3 alternativas = 18
opciones conceptuales). Los códigos y claves son PROVISIONALES hasta que la
diseñadora entregue los recursos y se cierre el contrato de capas (P06/P09);
el backend validará contra `catalog_options` cuando exista (P08).

Este catálogo empaquetado permite que el modo invitado funcione sin API.
Cuando el backend esté disponible, /api/catalog/ será la fuente de verdad.
"""

from __future__ import annotations

import zlib
from dataclasses import dataclass, replace

SCHEMA_VERSION = 1
PROVISIONAL = True
CATALOG_SOURCE = "bundled"


@dataclass(frozen=True)
class Option:
    code: str
    name: str
    description: str
    swatch: str  # color orientativo de la pieza (no es el asset final)
    asset_path: str = ""  # ruta provisional; vacía mientras no haya assets
    is_premium: bool = False


@dataclass(frozen=True)
class Category:
    key: str
    label: str
    short_label: str
    icon: str  # nombre de icono Material (ft.Icons)
    tagline: str
    options: tuple[Option, ...]


CATEGORIES: tuple[Category, ...] = (
    Category(
        key="fur",
        label="Pelaje",
        short_label="Pelaje",
        icon="palette",
        tagline="El lienzo de tu gato",
        options=(
            Option("tabby", "Atigrado naranja", "Rayas con actitud de lunes", "#F2A15A"),
            Option("bicolor", "Bicolor", "Mitad y mitad, como su personalidad", "#FFF0D8"),
            Option("dark_spots", "Manchas oscuras", "Misterio en cada manchita", "#5C5266"),
        ),
    ),
    Category(
        key="eyes",
        label="Ojos",
        short_label="Ojos",
        icon="visibility",
        tagline="La mirada lo dice todo",
        options=(
            Option("round_green", "Redondos verdes", "Curiosidad permanente", "#4DAD72"),
            Option("big_blue", "Grandes azules", "Drama nivel telenovela", "#5AA7E8"),
            Option("almond_amber", "Almendrados ámbar", "Elegancia felina", "#E8A13C"),
        ),
    ),
    Category(
        key="hair",
        label="Cabello",
        short_label="Cabello",
        icon="content_cut",
        tagline="Porque los gatos también tienen bad hair days",
        options=(
            Option("short_fringe", "Flequillo corto", "Práctico y adorable", "#684632"),
            Option("side_locks", "Mechones laterales", "Estilo sin esfuerzo", "#3E3A4D"),
            Option("wavy", "Cabello ondulado", "Volumen de otro nivel", "#C98A4B"),
        ),
    ),
    Category(
        key="top",
        label="Parte superior",
        short_label="Superior",
        icon="checkroom",
        tagline="Arriba del caos",
        options=(
            Option("tshirt", "Camiseta", "Básica nunca, aburrida jamás", "#FFB997"),
            Option("hoodie", "Sudadera", "Modo comfy activado", "#DBC6FF"),
            Option("shirt", "Camisa", "Formal, pero con bigotes", "#9AD0C2"),
        ),
    ),
    Category(
        key="bottom",
        label="Parte inferior",
        short_label="Inferior",
        icon="dry_cleaning",
        tagline="El complemento perfecto",
        options=(
            Option("shorts", "Pantalón corto", "Listo para la aventura", "#7B61FF"),
            Option("skirt", "Falda", "Giro incluido", "#F7D7E8"),
            Option("pants", "Pantalón largo", "Elegancia de pies a cola", "#4E4A5C"),
        ),
    ),
    Category(
        key="accessory",
        label="Accesorios",
        short_label="Extras",
        icon="star",
        tagline="El toque final de caos",
        options=(
            Option("glasses", "Gafas", "Intelectual, claramente", "#302B3A"),
            Option("bow", "Lazo", "Coqueto por naturaleza", "#FF6B6B"),
            Option("beanie", "Gorro", "Abrigo y estilo", "#FFD166"),
        ),
    ),
)

CATEGORY_KEYS = tuple(c.key for c in CATEGORIES)
_DEFAULT_CATEGORIES = CATEGORIES

_FALLBACK_PALETTE = (
    "#F2A15A", "#FFF0D8", "#5C5266", "#4DAD72", "#5AA7E8",
    "#E8A13C", "#684632", "#3E3A4D", "#C98A4B", "#FFB997",
    "#DBC6FF", "#9AD0C2", "#7B61FF", "#F7D7E8", "#4E4A5C",
    "#302B3A", "#FF6B6B", "#FFD166",
)


def _bundled_option(category_key: str, code: str) -> Option | None:
    for category in _DEFAULT_CATEGORIES:
        if category.key == category_key:
            return next((o for o in category.options if o.code == code), None)
    return None


def _fallback_swatch(category_key: str, code: str) -> str:
    index = zlib.crc32(f"{category_key}:{code}".encode("utf-8")) % len(_FALLBACK_PALETTE)
    return _FALLBACK_PALETTE[index]


def apply_api_catalog(payload: dict) -> bool:
    """Adopta el catálogo del backend conservando descripciones y colores locales.

    Devuelve False si el backend aún no tiene las seis categorías activas; en
    ese caso la interfaz mantiene el catálogo empaquetado y muestra el aviso
    correspondiente. Los códigos del backend son la autoridad.
    """
    global CATEGORIES, CATALOG_SOURCE
    if not isinstance(payload, dict):
        return False
    categories = payload.get("categories")
    if not isinstance(categories, dict) or not categories:
        return False

    rebuilt: list[Category] = []
    for base in _DEFAULT_CATEGORIES:
        entries = categories.get(base.key)
        if not isinstance(entries, list) or not entries:
            return False
        options: list[Option] = []
        seen: set[str] = set()
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            code = entry.get("code")
            if not isinstance(code, str) or not code or code in seen:
                continue
            seen.add(code)
            bundled = _bundled_option(base.key, code)
            options.append(
                Option(
                    code=code,
                    name=entry.get("label") or (bundled.name if bundled else code),
                    description=bundled.description if bundled else "Recurso provisional del catálogo.",
                    swatch=bundled.swatch if bundled else _fallback_swatch(base.key, code),
                    asset_path=entry.get("asset_path") or "",
                    is_premium=bool(entry.get("is_premium")),
                )
            )
        if not options:
            return False
        rebuilt.append(replace(base, options=tuple(options)))

    CATEGORIES = tuple(rebuilt)
    CATALOG_SOURCE = "api"
    return True


def reset_catalog() -> None:
    global CATEGORIES, CATALOG_SOURCE
    CATEGORIES = _DEFAULT_CATEGORIES
    CATALOG_SOURCE = "bundled"


def normalize_configuration(configuration: dict | None) -> dict:
    """Convierte la configuración del backend (`{"code": ...}`) al formato del editor.

    El backend normaliza cada categoría como objeto; la interfaz trabaja con el
    código de la opción. Las opciones desconocidas caen en la primera válida.
    """
    source = configuration if isinstance(configuration, dict) else {}
    normalized = {"schema_version": source.get("schema_version", SCHEMA_VERSION)}
    for category in CATEGORIES:
        block = source.get(category.key)
        if isinstance(block, str):
            code = block
        elif isinstance(block, dict):
            code = block.get("code") or block.get("style") or block.get("pattern")
        else:
            code = None
        if not isinstance(code, str) or not is_valid_option(category.key, code):
            code = category.options[0].code
        normalized[category.key] = code
    return normalized


def get_category(key: str) -> Category | None:
    return next((c for c in CATEGORIES if c.key == key), None)


def get_option(category_key: str, code: str) -> Option | None:
    cat = get_category(category_key)
    if cat is None:
        return None
    return next((o for o in cat.options if o.code == code), None)


def is_valid_option(category_key: str, code: str) -> bool:
    return get_option(category_key, code) is not None


def default_config() -> dict:
    """Configuración inicial: primera opción de cada categoría."""
    config = {"schema_version": SCHEMA_VERSION}
    for cat in CATEGORIES:
        config[cat.key] = cat.options[0].code
    return config


def validate_config(config: dict) -> list[str]:
    """Validación local de estructura y catálogo (el backend es la autoridad)."""
    errors: list[str] = []
    if not isinstance(config, dict):
        return ["La configuración debe ser un objeto."]
    if config.get("schema_version") != SCHEMA_VERSION:
        errors.append("Versión de esquema no soportada.")
    for key in CATEGORY_KEYS:
        code = config.get(key)
        if not isinstance(code, str) or not code:
            errors.append(f"Falta la categoría '{key}'.")
        elif not is_valid_option(key, code):
            errors.append(f"Opción '{code}' fuera del catálogo en '{key}'.")
    return errors


def config_summary(config: dict) -> list[tuple[str, str]]:
    """Pares (categoría, nombre de opción) para mostrar la combinación actual."""
    result = []
    for cat in CATEGORIES:
        opt = get_option(cat.key, config.get(cat.key, ""))
        result.append((cat.label, opt.name if opt else "—"))
    return result


def as_api_payload() -> dict:
    """Formato similar a GET /api/catalog/ (contrato provisional, P03/P08)."""
    return {
        "schema_version": SCHEMA_VERSION,
        "provisional": PROVISIONAL,
        "categories": {
            cat.key: [
                {"code": o.code, "name": o.name, "description": o.description}
                for o in cat.options
            ]
            for cat in CATEGORIES
        },
    }
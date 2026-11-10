"""Catálogo provisional del editor.

Fuente conceptual: docs/02_REQUIREMENTS.md (6 campos × 3 alternativas = 18
opciones conceptuales). Los códigos y claves son PROVISIONALES hasta que la
diseñadora entregue los recursos y se cierre el contrato de capas (P06/P09);
el backend validará contra `catalog_options` cuando exista (P08).

Este catálogo empaquetado permite que el modo invitado funcione sin API.
Cuando el backend esté disponible, /api/catalog/ será la fuente de verdad.
"""

from __future__ import annotations

from dataclasses import dataclass

SCHEMA_VERSION = 1
PROVISIONAL = True


@dataclass(frozen=True)
class Option:
    code: str
    name: str
    description: str
    swatch: str  # color orientativo de la pieza (no es el asset final)


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
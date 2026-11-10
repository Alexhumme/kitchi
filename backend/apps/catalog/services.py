"""Validación de la configuración del personaje contra el catálogo.

La regla de negocio está aquí, no en las vistas ni en la interfaz
(AGENTS.md: la validación y autorización residen en el backend).
El cliente no puede enviar rutas de archivo arbitrarias (04_DATA_MODEL.md).
"""

from django.conf import settings

from apps.core.errors import APIError

from .models import CatalogOption

CONFIG_SCHEMA_VERSION = 1

# Claves del documento y su categoría en el catálogo.
CATEGORY_KEYS = {
    "fur": "fur",
    "eyes": "eyes",
    "hair": "hair",
    "top": "top",
    "bottom": "bottom",
    "accessory": "accessory",
}

# Las opciones con color permitido se guardan como atributos de la categoría.
COLOR_KEYS_BY_CATEGORY = {
    "fur": ("base_color", "secondary_color"),
    "eyes": ("color",),
    "hair": ("color",),
}

HEX_LENGTHS = (7, 9)  # #RRGGBB y #RRGGBBAA


def _is_hex_color(value) -> bool:
    if not isinstance(value, str) or not value.startswith("#"):
        return False
    if len(value) not in HEX_LENGTHS:
        return False
    try:
        int(value[1:], 16)
    except ValueError:
        return False
    return True


def validate_configuration(configuration, user=None) -> dict:
    """Devuelve la configuración normalizada o lanza APIError con detalle por campo.

    Las opciones marcadas como premium solo se aceptan si `user` tiene el plan.
    """
    if not isinstance(configuration, dict):
        raise APIError("INVALID_CONFIGURATION", "La configuración del gato debe ser un objeto JSON.")

    version = configuration.get("schema_version", CONFIG_SCHEMA_VERSION)
    if version != CONFIG_SCHEMA_VERSION:
        raise APIError(
            "UNSUPPORTED_SCHEMA_VERSION",
            f"La versión de esquema {version} no es compatible con la actual ({CONFIG_SCHEMA_VERSION}).",
        )

    problems = {}
    allow_premium = user is None or getattr(user, "profile", None) is None or user.profile.premium
    unknown_keys = [key for key in configuration if key not in {"schema_version", *CATEGORY_KEYS}]
    if unknown_keys:
        problems["desconocidas"] = unknown_keys

    normalized = {"schema_version": CONFIG_SCHEMA_VERSION}
    for key, category in CATEGORY_KEYS.items():
        block = configuration.get(key)
        if block is None:
            problems[key] = "Falta la categoría."
            continue

        variant, colors = _split_block(block)
        option = CatalogOption.objects.filter(category=category, code=variant, is_active=True).first()
        if option is None:
            problems[key] = f"La opción «{variant}» no existe o está inactiva en {category}."
            continue
        if option.is_premium and not allow_premium:
            problems[key] = f"«{variant}» requiere el plan premium."
            continue

        color_error = _check_colors(category, colors)
        if color_error:
            problems[key] = color_error
            continue

        normalized[key] = {"code": variant, **{name: value for name, value in colors.items()}}

    if problems:
        raise APIError(
            "INVALID_CONFIGURATION",
            "La configuración usa recursos fuera del catálogo o incompletos.",
            details={"campos": problems},
        )
    return normalized


def _split_block(block):
    """Acepta `"hoodie"` o `{"style": "hoodie", "color": "#..."}`."""
    if isinstance(block, str):
        return block, {}
    if isinstance(block, dict):
        variant = block.get("style") or block.get("code") or block.get("pattern")
        colors = {k: v for k, v in block.items() if k.endswith("color")}
        return (variant if isinstance(variant, str) else None), colors
    return None, {}


def _check_colors(category, colors) -> str | None:
    allowed = COLOR_KEYS_BY_CATEGORY.get(category, ())
    unexpected = [name for name in colors if name not in allowed]
    if unexpected:
        return f"Colores no permitidos para {category}: {', '.join(sorted(unexpected))}."
    for name, value in colors.items():
        if not _is_hex_color(value):
            return f"«{name}» debe ser un color hexadecimal (#RRGGBB)."
    return None

"""Validación de la configuración del personaje contra el catálogo.

La regla de negocio vive en el backend. El cliente solo envía identificadores
de recursos y colores; nunca rutas de archivo arbitrarias.
"""

from apps.core.errors import APIError

from .models import CatalogOption

CONFIG_SCHEMA_VERSION = 1

CATEGORY_KEYS = {
    "fur": "fur",
    "eyes": "eyes",
    "hair": "hair",
    "top": "top",
    "bottom": "bottom",
}

COLOR_KEYS_BY_CATEGORY = {
    "fur": ("base_color", "secondary_color"),
    "eyes": ("color",),
    "hair": ("color",),
    "top": ("color",),
    "bottom": ("color",),
    "accessory": ("color",),
}

HEX_LENGTHS = (7, 9)


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


def _split_block(block):
    """Acepta un código legacy o un bloque `{code|style|pattern, ...colores}`."""
    if isinstance(block, str):
        return block, {}
    if isinstance(block, dict):
        variant = block.get("style") or block.get("code") or block.get("pattern")
        colors = {key: value for key, value in block.items() if key.endswith("color")}
        return (variant if isinstance(variant, str) else None), colors
    return None, {}


def _check_colors(category, colors) -> str | None:
    allowed = COLOR_KEYS_BY_CATEGORY.get(category, ())
    unexpected = [name for name in colors if name not in allowed]
    if unexpected:
        return f"Colores no permitidos para {category}: {', '.join(sorted(unexpected))}."
    for name, value in colors.items():
        if not _is_hex_color(value):
            return f"«{name}» debe ser un color hexadecimal (#RRGGBB o #RRGGBBAA)."
    return None


def _active_option(category: str, code: str):
    return CatalogOption.objects.filter(category=category, code=code, is_active=True).first()


def _normalize_accessories(raw, allow_premium: bool):
    if not isinstance(raw, list):
        return None, "Debe ser una lista de accesorios."
    normalized = []
    codes = set()
    groups = set()
    for index, block in enumerate(raw):
        if not isinstance(block, dict):
            return None, f"El accesorio {index} debe ser un objeto."
        code = block.get("code")
        if not isinstance(code, str) or not code:
            return None, f"El accesorio {index} no tiene código."
        unexpected = [key for key in block if key not in {"code", "color"}]
        if unexpected:
            return None, f"El accesorio {index} tiene campos no permitidos: {', '.join(sorted(unexpected))}."
        colors = {"color": block["color"]} if "color" in block else {}
        color_error = _check_colors("accessory", colors)
        if color_error:
            return None, f"El accesorio {index}: {color_error}"
        option = _active_option("accessory", code)
        if option is None:
            return None, f"El accesorio «{code}» no existe o está inactivo."
        if option.is_premium and not allow_premium:
            return None, f"«{code}» requiere el plan premium."
        if code in codes:
            return None, f"El accesorio «{code}» está repetido."
        group = option.compatibility_group or f"legacy:{code}"
        if group in groups:
            return None, f"Ya hay un accesorio del tipo «{option.compatibility_group or code}»."
        codes.add(code)
        groups.add(group)
        normalized.append({"code": code, **colors})
    return normalized, None


def _normalize_legacy_accessory(block, allow_premium: bool):
    code, colors = _split_block(block)
    if colors:
        return None, "El accesorio legacy no admite colores."
    option = _active_option("accessory", code) if isinstance(code, str) else None
    if option is None:
        return None, "El accesorio legacy no existe o está inactivo."
    if option.is_premium and not allow_premium:
        return None, f"«{code}» requiere el plan premium."
    return [{"code": code}], None


def validate_configuration(configuration, user=None) -> dict:
    """Normaliza la configuración o lanza APIError con el detalle por campo."""
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
    allowed_keys = {"schema_version", *CATEGORY_KEYS, "accessories", "accessory"}
    unknown_keys = [key for key in configuration if key not in allowed_keys]
    if unknown_keys:
        problems["desconocidas"] = unknown_keys

    normalized = {"schema_version": CONFIG_SCHEMA_VERSION}
    for key, category in CATEGORY_KEYS.items():
        block = configuration.get(key)
        if block is None:
            problems[key] = "Falta la categoría."
            continue
        variant, colors = _split_block(block)
        option = _active_option(category, variant) if isinstance(variant, str) else None
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
        normalized[key] = {"code": variant, **colors}

    accessories = None
    if "accessories" in configuration:
        accessories, error = _normalize_accessories(configuration["accessories"], allow_premium)
        if error:
            problems["accessories"] = error
    if "accessory" in configuration:
        legacy, error = _normalize_legacy_accessory(configuration["accessory"], allow_premium)
        if error:
            problems["accessory"] = error
        elif accessories is None:
            accessories = legacy
        elif not accessories:
            problems["accessory"] = "No puede enviar un accesorio legacy si accessories está vacío."
        elif legacy[0]["code"] != accessories[0]["code"]:
            problems["accessory"] = "Debe coincidir con el primer elemento de accessories."
    if accessories is None and "accessories" not in problems and "accessory" not in problems:
        problems["accessories"] = "Falta la lista de accesorios."

    if problems:
        raise APIError(
            "INVALID_CONFIGURATION",
            "La configuración usa recursos fuera del catálogo o incompletos.",
            details={"campos": problems},
        )

    normalized["accessories"] = accessories
    if accessories:
        normalized["accessory"] = {"code": accessories[0]["code"]}
    return normalized

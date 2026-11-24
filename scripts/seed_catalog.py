"""Siembra el catálogo del personaje y las seis poses en la base de datos.

Incluye los códigos legacy para que los gatos antiguos sigan siendo válidos y
los códigos de los assets SVG reales usados por el editor React. Es idempotente.

Uso:
    .venv\\Scripts\\python.exe scripts/seed_catalog.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from apps.catalog.models import CatalogOption, Pose  # noqa: E402

# category, code, label, asset_path, compatibility_group
OPTIONS: list[tuple[str, str, str, str, str]] = [
    ("fur", "tabby", "Atigrado naranja", "", ""),
    ("fur", "bicolor", "Bicolor", "", ""),
    ("fur", "dark_spots", "Manchas oscuras", "", ""),
    ("eyes", "round_green", "Redondos verdes", "", ""),
    ("eyes", "big_blue", "Grandes azules", "", ""),
    ("eyes", "almond_amber", "Almendrados ámbar", "", ""),
    ("hair", "anime_style", "Anime", "hair/anime_style_hair_back.svg", ""),
    ("hair", "short_bangs", "Flequillo corto", "hair/short_hair_in_the_back.svg", ""),
    ("hair", "cloud_bangs", "Nube", "hair/hair_back_medium.svg", ""),
    ("hair", "long_side", "Largo lateral", "hair/long_hair_in_the_back.svg", ""),
    ("hair", "short_hair", "Corto", "hair/short_hair_in_the_back.svg", ""),
    ("hair", "side_swept", "Barrido", "hair/hair_back_medium.svg", ""),
    ("hair", "triangular", "Triangular", "hair/short_hair_in_the_back.svg", ""),
    ("hair", "uneven", "Desigual", "hair/hair_back_medium.svg", ""),
    ("hair", "widows_peak", "Pico de viuda", "hair/short_hair_in_the_back.svg", ""),
    ("hair", "bob", "Bob", "hair/bob_haircutwith_volume_at_the_back.svg", ""),
    ("top", "polo_shirt", "Camisa polo", "tops/polo_shirt.svg", ""),
    ("top", "short_sleeved", "Manga corta", "tops/short_sleeved shirt.svg", ""),
    ("top", "long_sleeved", "Manga larga", "tops/long_sleeved shirt.svg", ""),
    ("top", "cuffed_shirt", "Puños", "tops/long_sleeved_shirt_with_cuffs.svg", ""),
    ("top", "bib_shirt", "Bordada", "tops/bib_front_shirt.svg", ""),
    ("top", "zipper_shirt", "Cremallera", "tops/shirt with_zipper.svg", ""),
    ("bottom", "denim_shorts", "Pantalón corto", "bottoms/denim_shorts.svg", ""),
    ("bottom", "long_trousers", "Pantalón largo", "bottoms/long_trousers.svg", ""),
    ("bottom", "sweat_pants", "Deportivo", "bottoms/sweat_pants.svg", ""),
    ("bottom", "flared_skirt", "Acampanada", "bottoms/flared_skirt.svg", ""),
    ("bottom", "greek_key_skirt", "Griega", "bottoms/greek_key_skirt.svg", ""),
    ("bottom", "pleated_skirt", "Plisada", "bottoms/pleated_skirt.svg", ""),
    ("accessory", "round_glasses", "Gafas redondas", "accessories/round_glasses.svg", "eyewear"),
    ("accessory", "big_glasses", "Gafas grandes", "accessories/glasses.svg", "eyewear"),
    ("accessory", "bow_tie", "Corbata de lazo", "accessories/bow_tie.svg", "neckwear"),
    ("accessory", "collar_tie", "Corbata", "accessories/collar_tie.svg", "neckwear"),
    ("accessory", "long_bow_tie", "Corbata larga", "accessories/long_bow_tie.svg", "neckwear"),
    ("accessory", "moustache", "Bigote", "accessories/moustache.svg", "facial_hair"),
    ("accessory", "pipe", "Pipa", "accessories/pipe.svg", "pipe"),
    ("accessory", "fedora", "Sombrero", "accessories/fedora_hat.svg", "headwear"),
    ("accessory", "winter_beanie", "Gorro de lana", "accessories/winter_beanie.svg", "headwear"),
    ("accessory", "three_pointed_crown", "Corona de 3", "accessories/3_pointed_crown.svg", "headwear"),
    ("accessory", "four_pointed_crown", "Corona de 4", "accessories/4_pointed_crown.svg", "headwear"),
    ("accessory", "hair_bows", "Lazos", "accessories/hair_bows.svg", "hair_bows"),
    ("accessory", "piccolo_antennas", "Antenas", "accessories/piccolo_antennas.svg", "headwear"),
    ("hair", "short_fringe", "Flequillo corto (legacy)", "", ""),
    ("hair", "side_locks", "Mechones laterales (legacy)", "", ""),
    ("hair", "wavy", "Cabello ondulado (legacy)", "", ""),
    ("top", "tshirt", "Camiseta (legacy)", "", ""),
    ("top", "hoodie", "Sudadera (legacy)", "", ""),
    ("top", "shirt", "Camisa (legacy)", "", ""),
    ("bottom", "shorts", "Pantalón corto (legacy)", "", ""),
    ("bottom", "skirt", "Falda (legacy)", "", ""),
    ("bottom", "pants", "Pantalón largo (legacy)", "", ""),
    ("accessory", "glasses", "Gafas (legacy)", "", ""),
    ("accessory", "bow", "Lazo (legacy)", "", ""),
    ("accessory", "beanie", "Gorro (legacy)", "", ""),
]

POSES = [
    ("greeting", "Saludo", "greeting/greetings.svg"),
    ("happy", "Alegría", "happy/happy.svg"),
    ("angry", "Enfado", "angry/angry.svg"),
    ("sad", "Tristeza", "sad/sad.svg"),
    ("surprised", "Sorpresa", "surprised/amazed.svg"),
    ("sleepy", "Sueño", "sleepy/asleep.svg"),
]


def main() -> int:
    created_options = 0
    updated_options = 0
    z_orders: dict[str, int] = {}
    for category, code, label, asset_path, group in OPTIONS:
        z_orders[category] = z_orders.get(category, 0) + 10
        asset = f"assets/characters/{asset_path}" if asset_path else ""
        _, created = CatalogOption.objects.update_or_create(
            category=category,
            code=code,
            defaults={
                "label": label,
                "asset_path": asset,
                "compatibility_group": group,
                "z_order": z_orders[category],
                "is_premium": False,
                "is_active": True,
            },
        )
        created_options += int(created)
        updated_options += int(not created)

    created_poses = 0
    updated_poses = 0
    for code, name, asset_path in POSES:
        _, created = Pose.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "asset_path": f"assets/poses/{asset_path}",
                "is_active": True,
            },
        )
        created_poses += int(created)
        updated_poses += int(not created)

    print(f"Catálogo sembrado ({len(OPTIONS)} opciones y {len(POSES)} poses).")
    print(f"Opciones: {created_options} creadas, {updated_options} actualizadas.")
    print(f"Poses: {created_poses} creadas, {updated_poses} actualizadas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

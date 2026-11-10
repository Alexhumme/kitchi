"""Siembra el catálogo provisional y las seis poses en la base de datos.

Mientras la diseñadora no entregue los recursos definitivos (P06/P08), la
interfaz usa placeholders de color. Este script registra esas mismas opciones
con códigos estables para que el backend pueda validar los gatos que guarda el
frontend. Es idempotente: se puede ejecutar varias veces.

Uso:
    .venv\\Scripts\\python.exe scripts/seed_catalog.py

Las rutas de `asset_path` apuntan a `assets/.../placeholder.png`; son rutas
provisionales, no archivos reales, y se sustituirán cuando lleguen los assets.
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

CATEGORIES: dict[str, list[tuple[str, str, int]]] = {
    "fur": [
        ("tabby", "Atigrado naranja", 10),
        ("bicolor", "Bicolor", 20),
        ("dark_spots", "Manchas oscuras", 30),
    ],
    "eyes": [
        ("round_green", "Redondos verdes", 40),
        ("big_blue", "Grandes azules", 50),
        ("almond_amber", "Almendrados ámbar", 60),
    ],
    "hair": [
        ("short_fringe", "Flequillo corto", 70),
        ("side_locks", "Mechones laterales", 80),
        ("wavy", "Cabello ondulado", 90),
    ],
    "top": [
        ("tshirt", "Camiseta", 100),
        ("hoodie", "Sudadera", 110),
        ("shirt", "Camisa", 120),
    ],
    "bottom": [
        ("shorts", "Pantalón corto", 130),
        ("skirt", "Falda", 140),
        ("pants", "Pantalón largo", 150),
    ],
    "accessory": [
        ("glasses", "Gafas", 160),
        ("bow", "Lazo", 170),
        ("beanie", "Gorro", 180),
    ],
}

POSES = [
    ("greeting", "Saludo"),
    ("happy", "Alegría"),
    ("angry", "Enfado"),
    ("sad", "Tristeza"),
    ("surprised", "Sorpresa"),
    ("sleepy", "Sueño"),
]


def main() -> int:
    created_options = 0
    updated_options = 0
    for category, options in CATEGORIES.items():
        for code, label, z_order in options:
            _, created = CatalogOption.objects.update_or_create(
                category=category,
                code=code,
                defaults={
                    "label": label,
                    "asset_path": f"assets/placeholders/{category}/{code}.png",
                    "z_order": z_order,
                    "is_premium": False,
                    "is_active": True,
                },
            )
            created_options += int(created)
            updated_options += int(not created)

    created_poses = 0
    updated_poses = 0
    for code, name in POSES:
        _, created = Pose.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "asset_path": f"assets/placeholders/poses/{code}.png",
                "is_active": True,
            },
        )
        created_poses += int(created)
        updated_poses += int(not created)

    print("Catálogo provisional sembrado (18 opciones y 6 poses).")
    print(f"Opciones: {created_options} creadas, {updated_options} actualizadas.")
    print(f"Poses: {created_poses} creadas, {updated_poses} actualizadas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

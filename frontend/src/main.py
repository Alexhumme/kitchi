"""Punto de entrada del frontend Flet Web de Kitchi Studio.

Uso documentado:
    flet run frontend/src/main.py --web --port 8550

También funciona con:
    python frontend/src/main.py
"""

from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = SRC_DIR.parent
sys.path.insert(0, str(SRC_DIR))

import flet as ft  # noqa: E402

from kitchi.app import main  # noqa: E402

if __name__ == "__main__":
    ft.run(
        main,
        view=ft.AppView.WEB_BROWSER,
        port=8550,
        assets_dir=str(FRONTEND_DIR / "assets"),
    )

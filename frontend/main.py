"""Punto de entrada del frontend Flet Web de Kitchi Studio.

Uso: python frontend/main.py  → http://localhost:8550
"""

from pathlib import Path
import sys

FRONTEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(FRONTEND_DIR / "src"))

import flet as ft  # noqa: E402

from kitchi.app import main  # noqa: E402

if __name__ == "__main__":
    ft.run(
        main,
        view=ft.AppView.WEB_BROWSER,
        port=8550,
        assets_dir=str(FRONTEND_DIR / "assets"),
    )
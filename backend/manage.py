#!/usr/bin/env python
"""Utilidades de línea de órdenes del backend de Kitchi Studio."""
import os
import sys
from pathlib import Path

# Permite ejecutar `python manage.py ...` sin instalar el proyecto como paquete.
sys.path.insert(0, str(Path(__file__).resolve().parent))


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

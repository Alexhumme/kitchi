"""Configuración de pruebas: mismo código que desarrollo, persistencia en SQLite.

La base de datos de pruebas necesita privilegios de CREATE DATABASE que el
usuario de desarrollo MySQL no tiene; SQLite mantiene las pruebas rápidas y
reproducibles sin tocar los permisos del servidor. Las migraciones reales se
verifican contra MySQL con `manage.py migrate`.
"""

import os

os.environ["DB_ENGINE"] = "sqlite"

from .settings import *  # noqa: F401,F403,E402

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST": {"NAME": ":memory:"},
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

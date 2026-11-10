"""Verificación manual del backend contra el servidor en marcha (MySQL).

Uso:
    cd backend && python manage.py runserver        # en una consola
    python scripts/check_backend.py                 # en otra

Las cuentas y gatos de prueba se crean con sufijo de marca de tiempo y se
eliminan al terminar con la ORM, para no dejar datos de prueba en la base.
No sustituye la suite automatizada de backend/tests.
"""

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "http://127.0.0.1:8000"
SUFFIX = sys.argv[1] if len(sys.argv) > 1 else str(int(time.time()))
PASSWORD = "HojaDeStickers2026"

CONFIGURATION = {
    "schema_version": 1,
    "fur": {"pattern": "tabby", "base_color": "#F2A15A", "secondary_color": "#FFF0D8"},
    "eyes": {"style": "round", "color": "#4DAD72"},
    "hair": {"style": "short_fringe", "color": "#684632"},
    "top": "hoodie",
    "bottom": "shorts",
    "accessory": "bow",
}

CREATED_USERNAMES = []


def call(method, path, payload=None, token=None):
    body = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(BASE + path, data=body, method=method)
    request.add_header("Content-Type", "application/json")
    if token:
        request.add_header("Authorization", f"Token {token}")
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, _decode(response.read().decode(), response.headers.get("Content-Type", ""))
    except urllib.error.HTTPError as error:
        return error.code, _decode(error.read().decode(), error.headers.get("Content-Type", ""))


def _decode(raw, content_type):
    if not raw:
        return None
    if "json" not in content_type:
        return {"_html": True}
    return json.loads(raw)


def register(username, email):
    CREATED_USERNAMES.append(username)
    status, body = call(
        "POST", "/api/auth/register/", {"username": username, "email": email, "password": PASSWORD}
    )
    return status, (body or {}).get("token")


def main() -> int:
    results = []

    def check(name, ok, detail=""):
        results.append((name, ok))
        print(f"{'OK  ' if ok else 'FALLO'} {name} {detail}")

    try:
        seed_catalog()
        status, health = call("GET", "/api/health/")
        check("health", status == 200 and health["database"] == "up", str(health))

        username = f"smoke_{SUFFIX}"
        status, token = register(username, f"smoke_{SUFFIX}@example.test")
        check("registro entrega token", status == 201 and bool(token))

        status, _ = register(f"otro_{SUFFIX}", f"otro{SUFFIX}@example.test")
        check("segunda cuenta creada", status == 201)

        status, _ = call(
            "POST",
            "/api/auth/register/",
            {"username": username, "email": f"dup{SUFFIX}@example.test", "password": PASSWORD},
        )
        check("usuario duplicado rechazado (400)", status == 400)

        status, logged = call("POST", "/api/auth/login/", {"username": username, "password": PASSWORD})
        check("login con credenciales validas", status == 200 and logged["token"] == token)

        status, _ = call("POST", "/api/auth/login/", {"username": username, "password": "incorrecta"})
        check("login invalido (401)", status == 401)

        status, me = call("GET", "/api/auth/me/", token=token)
        check("me devuelve el usuario actual", status == 200 and me["username"] == username, f"rol={me['role']}")

        status, _ = call("GET", "/api/auth/me/")
        check("me sin token (401)", status == 401)

        status, catalog = call("GET", "/api/catalog/")
        categories = list((catalog or {}).get("categories", {}))
        check("catalogo publico", status == 200, f"categorias={categories}")
        if categories:
            for category, options in catalog["categories"].items():
                code = options[0]["code"]
                current = CONFIGURATION.get(category)
                if isinstance(current, dict):
                    variant_key = "pattern" if category == "fur" else "style"
                    CONFIGURATION[category] = {**current, variant_key: code}
                else:
                    CONFIGURATION[category] = code

        ids = []
        for index in range(3):
            status, cat = call(
                "POST", "/api/cats/", {"name": f"Smoke{SUFFIX}-{index}", "configuration": CONFIGURATION}, token=token
            )
            if status == 201:
                ids.append(cat["id"])
        check("crear tres gatos", len(ids) == 3, f"ids={ids}")

        status, error = call(
            "POST", "/api/cats/", {"name": f"Smoke{SUFFIX}-x", "configuration": CONFIGURATION}, token=token
        )
        check("el cuarto gato se rechaza (409)", status == 409, str((error or {}).get("error", {}).get("code")))

        bad = dict(CONFIGURATION, top="recurso_inexistente")
        status, error = call("POST", "/api/cats/", {"name": f"Smoke{SUFFIX}-malo", "configuration": bad}, token=token)
        check("configuracion fuera de catalogo (400)", status == 400, str((error or {}).get("error", {}).get("code")))

        if ids:
            cat_id = ids[0]
            status, cat = call("GET", f"/api/cats/{cat_id}/", token=token)
            check("recuperar un gato guardado", status == 200 and cat["name"].startswith("Smoke"))

            status, _ = call("PATCH", f"/api/cats/{cat_id}/", {"name": f"Renombrado{SUFFIX}"}, token=token)
            check("actualizar la configuracion", status == 200)

            _, other_body = call(
                "POST", "/api/auth/login/", {"username": f"otro_{SUFFIX}", "password": PASSWORD}
            )
            status, _ = call("GET", f"/api/cats/{cat_id}/", token=(other_body or {}).get("token"))
            check("el gato de otro usuario no se lee (403)", status == 403, f"observed={status}")

            status, _ = call("DELETE", f"/api/cats/{cat_id}/", token=token)
            check("eliminar el gato propio", status == 204)

        status, _ = call("POST", "/api/auth/logout/", token=token)
        check("logout", status == 204)

        status, _ = call("GET", "/api/auth/me/", token=token)
        check("el token queda invalidado tras el logout", status == 401)

        status, _ = call("GET", "/api/docs/")
        check("Swagger UI responde", status == 200)
    finally:
        cleanup()

    failed = [name for name, ok in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} comprobaciones superadas")
    if failed:
        print("Pendientes: " + ", ".join(failed))
    return 1 if failed else 0


def _django():
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import django

    django.setup()


def seed_catalog():
    """Garantiza al menos una opción activa por categoría durante la verificación.

    El catálogo definitivo depende de los recursos de la diseñadora (P06/P08);
    estas filas se marcan con prefijo `smoke_` y se eliminan al terminar.
    """
    _django()
    from apps.catalog.models import CatalogOption, Pose

    defaults = {"fur": "tabby", "eyes": "round", "hair": "short_fringe", "top": "hoodie",
                "bottom": "shorts", "accessory": "bow"}
    for category, code in defaults.items():
        if not CatalogOption.objects.filter(category=category, is_active=True).exists():
            CatalogOption.objects.create(category=category, code=f"smoke_{code}", label="Prueba técnica",
                                         asset_path="", z_order=1)
    if not Pose.objects.filter(is_active=True).exists():
        for index, code in enumerate(["greeting", "happy", "angry", "sad", "surprised", "sleepy"]):
            Pose.objects.create(code=f"smoke_{code}", name="Prueba técnica")


def cleanup():
    """Borra por ORM las cuentas y las filas de catálogo creadas por esta verificación."""
    _django()
    from django.contrib.auth.models import User

    from apps.catalog.models import CatalogOption, Pose

    users, _ = User.objects.filter(username__in=CREATED_USERNAMES).delete()
    options = CatalogOption.objects.filter(code__startswith="smoke_").delete()[0]
    poses = Pose.objects.filter(code__startswith="smoke_").delete()[0]
    print(f"Limpieza: {users} cuentas, {options} opciones y {poses} poses de prueba eliminadas.")


if __name__ == "__main__":
    raise SystemExit(main())

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.cats.models import Cat

from .conftest import FULL_CONFIGURATION


def _payload(name="Michi", configuration=None):
    return {"name": name, "configuration": configuration or FULL_CONFIGURATION}


def _client_for(username):
    other = User.objects.create_user(username=username, password="OtraClaveSegura1")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {Token.objects.create(user=other).key}")
    return client


def test_crear_y_recuperar_gato(member_client, catalog, db):
    created = member_client.post("/api/cats/", _payload(), format="json")
    assert created.status_code == 201
    cat_id = created.json()["id"]

    detail = member_client.get(f"/api/cats/{cat_id}/")
    assert detail.status_code == 200
    assert detail.json()["configuration"]["fur"]["base_color"] == "#F2A15A"


def test_gato_inexistente_usa_404_normalizado(member_client, catalog, db):
    response = member_client.get("/api/cats/999999/")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "CAT_NOT_FOUND"


def test_no_se_lee_el_gato_de_otro_usuario(member_client, catalog, db):
    mine = member_client.post("/api/cats/", _payload(), format="json").json()["id"]
    other_client = _client_for("otra")

    assert other_client.get(f"/api/cats/{mine}/").status_code == 403
    assert other_client.get("/api/cats/").json()["results"] == []


def test_actualizar_configuracion(member_client, catalog, db):
    cat_id = member_client.post("/api/cats/", _payload(), format="json").json()["id"]
    nueva = {**FULL_CONFIGURATION, "eyes": {"style": "round", "color": "#111111"}}
    updated = member_client.patch(f"/api/cats/{cat_id}/", {"configuration": nueva}, format="json")
    assert updated.status_code == 200
    assert updated.json()["configuration"]["eyes"]["color"] == "#111111"


def test_eliminar_gato_propio(member_client, catalog, db):
    cat_id = member_client.post("/api/cats/", _payload(), format="json").json()["id"]
    assert member_client.delete(f"/api/cats/{cat_id}/").status_code == 204
    assert not Cat.objects.filter(pk=cat_id).exists()


def test_limite_tres_gatos_con_error_409(member_client, catalog, db, settings):
    settings.MAX_CATS_PER_USER = 3
    for index in range(3):
        assert member_client.post("/api/cats/", _payload(name=f"Michi{index}"), format="json").status_code == 201

    rejected = member_client.post("/api/cats/", _payload(name="Michi3"), format="json")
    assert rejected.status_code == 409
    error = rejected.json()["error"]
    assert error["code"] == "CAT_LIMIT_REACHED"
    assert error["details"]["limite"] == 3


def test_configuracion_fuera_de_catalogo_es_400(member_client, catalog, db):
    bad = {**FULL_CONFIGURATION, "top": "armadura_inexistente"}
    response = member_client.post("/api/cats/", _payload(configuration=bad), format="json")
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "INVALID_CONFIGURATION"
    assert "top" in error["details"]["campos"]


def test_color_invalido_es_400(member_client, catalog, db):
    bad = {**FULL_CONFIGURATION, "eyes": {"style": "round", "color": "rojo"}}
    response = member_client.post("/api/cats/", _payload(configuration=bad), format="json")
    assert response.status_code == 400
    assert "eyes" in response.json()["error"]["details"]["campos"]


def test_version_de_esquema_incompatible(member_client, catalog, db):
    response = member_client.post(
        "/api/cats/", _payload(configuration={**FULL_CONFIGURATION, "schema_version": 99}), format="json"
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "UNSUPPORTED_SCHEMA_VERSION"


def test_invitado_no_puede_escribir_en_el_catalogo(anon_client, catalog, db):
    """El catálogo solo lo escribe el rol admin (matriz RBAC de ADR-005)."""
    assert anon_client.get("/api/catalog/").status_code == 200
    assert anon_client.post("/api/cats/", _payload(), format="json").status_code == 401

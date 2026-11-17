"""Pruebas del hub: publicar, listar público y perfil público (P18)."""

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .conftest import FULL_CONFIGURATION


@pytest.fixture
def cat_id(member_client, catalog, db):
    created = member_client.post(
        "/api/cats/", {"name": "Michi", "configuration": FULL_CONFIGURATION}, format="json"
    )
    assert created.status_code == 201
    return created.json()["id"]


def _client_for(username: str) -> APIClient:
    other = User.objects.create_user(username=username, password="OtraClaveSegura1")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {Token.objects.create(user=other).key}")
    return client


def _publish(client, cat_id, title="Miau", visibility="public"):
    return client.post(
        "/api/publications/",
        {"cat_id": cat_id, "title": title, "description": "El primero", "visibility": visibility},
        format="json",
    )


# --- publicación ---------------------------------------------------------

def test_publicar_gato_y_verlo_en_el_feed_y_el_detalle(member_client, cat_id, catalog, db):
    created = _publish(member_client, cat_id)
    assert created.status_code == 201
    data = created.json()
    assert data["title"] == "Miau"
    assert data["author"] == "alex"
    assert data["cat"]["configuration"]["fur"]["base_color"] == "#F2A15A"

    feed = member_client.get("/api/publications/")
    assert feed.status_code == 200
    titles = [item["title"] for item in feed.json()["results"]]
    assert "Miau" in titles

    detail = member_client.get(f"/api/publications/{data['id']}/")
    assert detail.status_code == 200
    assert detail.json()["author"] == "alex"


def test_publicar_el_gato_de_otro_es_403(member_client, cat_id, catalog, db):
    other_client = _client_for("otra")
    response = _publish(other_client, cat_id)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN_CAT"


def test_publicar_gato_inexistente_es_404(member_client, catalog, db):
    response = _publish(member_client, 999999)
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "CAT_NOT_FOUND"


def test_publicar_dos_veces_el_mismo_gato_es_409(member_client, cat_id, catalog, db):
    assert _publish(member_client, cat_id).status_code == 201
    repeated = _publish(member_client, cat_id)
    assert repeated.status_code == 409
    assert repeated.json()["error"]["code"] == "PUBLICATION_ALREADY_EXISTS"


def test_invitado_no_puede_publicar(anon_client, cat_id, catalog, db):
    response = anon_client.post(
        "/api/publications/",
        {"cat_id": cat_id, "title": "Miau", "visibility": "public"},
        format="json",
    )
    assert response.status_code == 401


def _anon(path: str) -> APIClient:
    return APIClient().get(path)


# --- feed público ---------------------------------------------------------

def test_invitado_ve_el_feed_publico_y_solo_lo_publico(member_client, cat_id, catalog, db):
    _publish(member_client, cat_id, visibility="public")
    resultado = _anon("/api/publications/")
    assert resultado.status_code == 200
    assert [item["title"] for item in resultado.json()["results"]] == ["Miau"]


def test_la_publicacion_privada_no_la_ve_otra_persona(anon_client, member_client, cat_id, catalog, db):
    _publish(member_client, cat_id, visibility="private")
    other_client = _client_for("otra")
    anon_results = anon_client.get("/api/publications/").json()["results"]
    other_results = other_client.get("/api/publications/").json()["results"]
    own_results = member_client.get("/api/publications/").json()["results"]
    assert all(item["title"] != "Miau" for item in anon_results)
    assert all(item["title"] != "Miau" for item in other_results)
    assert any(item["title"] == "Miau" for item in own_results)


def test_la_busqueda_filtra_por_titulo_y_autor(member_client, cat_id, catalog, db):
    _publish(member_client, cat_id, title="Gato atigrado")
    por_titulo = member_client.get("/api/publications/?q=atigrado").json()["results"]
    por_autor = member_client.get("/api/publications/?q=alex").json()["results"]
    sin_resultados = member_client.get("/api/publications/?q=zzzz").json()["results"]
    assert any(item["title"] == "Gato atigrado" for item in por_titulo)
    assert any(item["author"] == "alex" for item in por_autor)
    assert sin_resultados == []


def test_la_busqueda_filtra_por_usuario(member_client, cat_id, catalog, db):
    _publish(member_client, cat_id)
    por_usuario = member_client.get("/api/publications/?user=alex").json()["results"]
    otra_cuenta = member_client.get("/api/publications/?user=nadie").json()["results"]
    assert len(por_usuario) == 1
    assert otra_cuenta == []


# --- perfil público -------------------------------------------------------

def test_perfil_publico_devuelve_usuario_gatos_y_publicaciones(member_client, cat_id, catalog, db):
    _publish(member_client, cat_id)
    response = _anon("/api/profiles/alex/")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alex"
    assert data["publication_count"] == 1
    assert data["cats"][0]["name"] == "Michi"
    assert data["publications"][0]["author"] == "alex"


def test_perfil_inexistente_es_404(anon_client, catalog, db):
    response = anon_client.get("/api/profiles/nadie/")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "PROFILE_NOT_FOUND"

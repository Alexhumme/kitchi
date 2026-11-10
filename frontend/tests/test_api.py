"""Pruebas del cliente API: modo local y contrato HTTP contra el mock."""

import json
import threading
from http.server import ThreadingHTTPServer

import pytest

from kitchi.api import ApiClient, ApiError


def test_local_mode_catalog():
    client = ApiClient("")
    assert client.mode == "local"
    payload = client.get_catalog()
    assert payload["provisional"] is True
    assert len(payload["categories"]) == 6
    assert len(client.get_poses()) == 6
    assert client.get_publications()["count"] == 0


@pytest.fixture()
def mock_server():
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
    from mock_api import MockHandler

    server = ThreadingHTTPServer(("127.0.0.1", 0), MockHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


def test_http_mode_against_mock(mock_server):
    client = ApiClient(mock_server)
    assert client.mode == "http"
    assert client.health()["simulated"] is True
    payload = client.get_catalog()
    assert payload["simulated"] is True
    assert len(payload["categories"]) == 6
    assert len(client.get_poses()) == 6
    assert client.get_publications()["results"] == []


def test_http_error_contract(mock_server):
    client = ApiClient(mock_server)
    with pytest.raises(ApiError) as exc:
        client._get("/api/no-existe/")
    assert exc.value.status == 404
    assert exc.value.code == "NOT_IMPLEMENTED_IN_MOCK"


def test_unreachable_api():
    client = ApiClient("http://127.0.0.1:1")
    with pytest.raises(ApiError) as exc:
        client.health()
    assert exc.value.code == "API_UNREACHABLE"


def test_auth_and_cats_payloads(monkeypatch):
    client = ApiClient("http://api.test")
    calls = []

    def fake_request(method, path, data=None, token=None):
        calls.append((method, path, data))
        if path == "/api/auth/register/":
            return {"token": "abc", "user": {"username": data["username"], "role": "member"}}
        if path == "/api/auth/login/":
            return {"token": "abc", "user": {"username": data["username"], "role": "member"}}
        if path == "/api/cats/" and method == "GET":
            return {"count": 1, "results": [{"id": 1, "name": "Michi", "configuration": {}}]}
        if path == "/api/cats/":
            return {"id": 1, "name": data.get("name"), "configuration": {}}
        if method == "PATCH":
            return {"id": 1, "name": data.get("name"), "configuration": {}}
        if method == "DELETE":
            return {}
        return {}

    monkeypatch.setattr(client, "_request", fake_request)
    assert client.register("michi", "michi@example.test", "secreto123")["token"] == "abc"
    assert client.login("michi", "secreto123")["token"] == "abc"
    assert client.list_cats()[0]["name"] == "Michi"
    assert client.create_cat("Michi", {"fur": "tabby"})["id"] == 1
    assert client.update_cat(1, "Otra", {"fur": "bicolor"})["name"] == "Otra"
    client.delete_cat(1)
    assert ("POST", "/api/auth/login/", {"username": "michi", "password": "secreto123"}) in calls


def test_api_error_uses_field_detail():
    error = ApiError("HTTP_400", "Los datos enviados no son válidos.", 400,
                     {"campo": {"password": ["La contraseña es demasiado corta."]}})
    assert error.user_message() == "La contraseña es demasiado corta."


def test_api_error_uses_catalog_detail():
    error = ApiError("INVALID_CONFIGURATION", "La configuración no es válida.", 400,
                     {"campos": ["Opción 'x' fuera del catálogo en 'fur'."]})
    assert error.user_message() == "Opción 'x' fuera del catálogo en 'fur'."
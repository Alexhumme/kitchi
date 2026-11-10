"""Pruebas del cliente API: modo local y contrato HTTP contra el mock."""

import json
import threading
from http.server import ThreadingHTTPServer

import pytest

from kitchi.api import ApiClient, ApiError


def test_local_mode_catalog():
    client = ApiClient()
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
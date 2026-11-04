def test_health_informa_disponibilidad(anon_client, db):
    response = anon_client.get("/api/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["database"] == "up"


def test_schema_openapi_se_genera(anon_client, db):
    response = anon_client.get("/api/schema/")
    assert response.status_code == 200
    assert b"openapi" in response.content


def test_swagger_ui_disponible(anon_client, db):
    assert anon_client.get("/api/docs/").status_code == 200

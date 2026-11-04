def test_catalog_publico_agrupa_por_categoria(anon_client, catalog, db):
    response = anon_client.get("/api/catalog/")
    assert response.status_code == 200
    body = response.json()
    assert body["schema_version"] == 1
    assert set(body["categories"]) == set(catalog)
    assert body["categories"]["fur"][0]["code"] == "tabby"


def test_poses_publicas(anon_client, catalog, db):
    response = anon_client.get("/api/poses/")
    assert response.status_code == 200
    body = response.json()
    assert "results" in body, "los listados devuelven paginación"
    codes = {pose["code"] for pose in body["results"]}
    assert codes == {"greeting", "happy", "angry", "sad", "surprised", "sleepy"}

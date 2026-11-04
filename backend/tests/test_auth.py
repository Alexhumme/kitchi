from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def test_register_crea_cuenta_perfil_y_token(anon_client, db):
    response = anon_client.post(
        "/api/auth/register/",
        {"username": "nova", "email": "nova@example.test", "password": "SuficientementeLarga1"},
        format="json",
    )
    assert response.status_code == 201
    body = response.json()
    assert body["user"]["role"] == "member"
    assert body["token"]
    created = User.objects.get(username="nova")
    assert created.profile.role == "member"
    assert created.password != "SuficientementeLarga1", "la contraseña debe quedar hasheada"


def test_register_rechaza_usuario_repetido(anon_client, user, db):
    response = anon_client.post(
        "/api/auth/register/",
        {"username": "alex", "email": "otro@example.test", "password": "SuficientementeLarga1"},
        format="json",
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "HTTP_400"


def test_login_devuelve_token_y_logout_lo_invalida(anon_client, user, db):
    login = anon_client.post(
        "/api/auth/login/", {"username": "alex", "password": "Contrasena123!"}, format="json"
    )
    assert login.status_code == 200
    token = login.json()["token"]

    authenticated = anon_client.get("/api/auth/me/", HTTP_AUTHORIZATION=f"Token {token}")
    assert authenticated.status_code == 200
    assert authenticated.json()["username"] == "alex"

    logout = anon_client.post("/api/auth/logout/", HTTP_AUTHORIZATION=f"Token {token}")
    assert logout.status_code == 204
    assert not Token.objects.filter(key=token).exists()
    assert anon_client.get("/api/auth/me/", HTTP_AUTHORIZATION=f"Token {token}").status_code == 401


def test_login_con_credenciales_incorrectas(anon_client, user, db):
    response = anon_client.post(
        "/api/auth/login/", {"username": "alex", "password": "incorrecta"}, format="json"
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_me_sin_autenticar_usa_formato_de_error(anon_client, db):
    response = anon_client.get("/api/auth/me/")
    assert response.status_code == 401
    assert set(response.json()["error"]) == {"code", "message", "details"}

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.catalog.models import CatalogOption, Pose

FULL_CONFIGURATION = {
    "schema_version": 1,
    "fur": {"pattern": "tabby", "base_color": "#F2A15A", "secondary_color": "#FFF0D8"},
    "eyes": {"style": "round", "color": "#4DAD72"},
    "hair": {"style": "short_fringe", "color": "#684632"},
    "top": "hoodie",
    "bottom": "shorts",
    "accessory": "bow",
}

DEFAULT_POSES = ["greeting", "happy", "angry", "sad", "surprised", "sleepy"]


@pytest.fixture
def catalog(db):
    """Catálogo mínimo equivalente al contrato inicial de la diseñadora."""
    options = {
        "fur": "tabby",
        "eyes": "round",
        "hair": "short_fringe",
        "top": "hoodie",
        "bottom": "shorts",
        "accessory": "bow",
    }
    for category, code in options.items():
        CatalogOption.objects.create(category=category, code=code, label=code.title())
    for code in DEFAULT_POSES:
        Pose.objects.create(code=code, name=code.title())
    return options


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alex", email="alex@example.test", password="Contrasena123!")


@pytest.fixture
def member_client(user):
    token, _ = Token.objects.get_or_create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


@pytest.fixture
def admin_client(user):
    user.profile.role = "admin"
    user.profile.save()
    token, _ = Token.objects.get_or_create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


@pytest.fixture
def anon_client():
    return APIClient()

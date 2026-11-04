"""Reglas de negocio de los personajes: límite del plan gratuito y validación."""

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction

from apps.catalog.services import validate_configuration
from apps.core.errors import APIError

from .models import Cat


def create_cat(user, name: str, configuration: dict) -> Cat:
    """Crea un gato validando catálogo y límite de tres en una sola transacción.

    El `select_for_update` sobre la fila del usuario serializa las creaciones
    simultáneas para que dos peticiones paralelas no excedan el límite.
    """
    normalized = validate_configuration(configuration, user=user)
    with transaction.atomic():
        locked_user = User.objects.select_for_update().get(pk=user.pk)
        current = Cat.objects.filter(user=locked_user).count()
        if current >= settings.MAX_CATS_PER_USER:
            raise APIError(
                "CAT_LIMIT_REACHED",
                f"El plan gratuito permite hasta {settings.MAX_CATS_PER_USER} gatos guardados.",
                http_status=409,
                details={"limite": settings.MAX_CATS_PER_USER, "actuales": current},
            )
        return Cat.objects.create(user=locked_user, name=name, configuration=normalized)


def update_cat(cat: Cat, configuration: dict, name: str | None = None) -> Cat:
    cat.configuration = validate_configuration(configuration, user=cat.user)
    if name is not None:
        cat.name = name
    cat.save()
    return cat

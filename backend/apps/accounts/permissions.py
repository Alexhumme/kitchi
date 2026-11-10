from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import SAFE_METHODS, BasePermission

ROLE_MEMBER = "member"
ROLE_ADMIN = "admin"

WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
ALL_METHODS = set(SAFE_METHODS) | WRITE_METHODS

# Recursos del sistema y su política base (ADR-005).
#   owned  → el dueño opera sobre sus registros; el admin sobre todos.
#   shared → lectura pública para usuarios autenticados, escritura solo admin.
RESOURCES = {
    "catalogoption": "shared",
    "pose": "shared",
    "cat": "owned",
    "stickerpack": "owned",
    "sticker": "owned",
    "publication": "owned",
    "generationjob": "owned",
}

ROLE_MATRIX = {
    ROLE_MEMBER: {"owned": ALL_METHODS, "shared": set(SAFE_METHODS)},
    ROLE_ADMIN: {"owned": ALL_METHODS, "shared": ALL_METHODS},
}


def role_of(user) -> str:
    profile = getattr(user, "profile", None)
    return profile.role if profile is not None else ROLE_MEMBER


def resolve_resource(obj=None, view=None) -> str | None:
    if obj is not None:
        return RESOURCES.get(obj._meta.model_name)
    model = getattr(view, "queryset", None)
    if model is not None:
        model = model.model
    name = getattr(view, "rbac_resource", None)
    if name is None and model is not None:
        name = model._meta.model_name
    return RESOURCES.get(name)


def owner_of(obj):
    """Dueño del registro: enlace directo `user`, autor del trabajo o dueño del gato."""
    for attribute in ("user", "created_by"):
        if hasattr(obj, attribute):
            return getattr(obj, attribute)
    cat = getattr(obj, "cat", None)
    return cat.user if cat is not None else None


class RoleBasedAccessPermission(BasePermission):
    """RBAC por rol y por recurso, con propiedad de recurso para los `owned`.

    Los recursos públicos (catálogo, poses, hub de publicaciones) se marcan en
    la vista con `rbac_public = True`; las vistas propias filtran por usuario en
    `get_queryset` y esta clase refuerza el permiso a nivel de objeto.
    """

    def has_permission(self, request, view):
        if getattr(view, "rbac_public", False) and request.method in SAFE_METHODS:
            return True
        user = request.user
        if not (user and user.is_authenticated):
            raise NotAuthenticated()
        # Un recurso sin declarar se trata como compartido: mínimo privilegio.
        resource = resolve_resource(view=view) or "shared"
        allowed = ROLE_MATRIX.get(role_of(user), {}).get(resource, set())
        return request.method in allowed

    def has_object_permission(self, request, view, obj):
        user = request.user
        if role_of(user) == ROLE_ADMIN:
            return True
        return resolve_resource(obj=obj) == "owned" and owner_of(obj) == user

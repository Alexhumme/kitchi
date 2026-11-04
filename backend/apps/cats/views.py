from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import ROLE_ADMIN, RoleBasedAccessPermission, role_of
from apps.community.models import Publication
from apps.core.errors import APIError

from .models import Cat
from .serializers import CatSerializer
from .services import create_cat, update_cat


class CatListCreateView(ListCreateAPIView):
    """`GET/POST /api/cats/`: lista los gatos propios y crea uno con el límite aplicado."""

    serializer_class = CatSerializer
    rbac_resource = "cat"

    def get_queryset(self):
        queryset = Cat.objects.select_related("user").order_by("-created_at")
        if role_of(self.request.user) == ROLE_ADMIN:
            return queryset
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cat = create_cat(
            user=request.user,
            name=serializer.validated_data["name"],
            configuration=serializer.validated_data["configuration"],
        )
        return Response(CatSerializer(cat).data, status=status.HTTP_201_CREATED)


class CatDetailView(APIView):
    """`GET/PATCH/DELETE /api/cats/{id}/`: acceso restringido al dueño o a un admin."""

    permission_classes = [RoleBasedAccessPermission]
    rbac_resource = "cat"
    serializer_class = CatSerializer

    def _get_cat(self, pk):
        cat = Cat.objects.filter(pk=pk).select_related("user").first()
        if cat is None:
            raise APIError("CAT_NOT_FOUND", "El gato solicitado no existe.", http_status=404)
        return cat

    def get(self, request, pk):
        cat = self._get_cat(pk)
        if not self._allowed_to_read(request, cat):
            self.permission_denied(request, message="No puedes ver el gato de otro usuario.")
        return Response(CatSerializer(cat).data)

    def _allowed_to_read(self, request, cat) -> bool:
        """El dueño y el admin siempre; cualquier otro solo si está publicado (05_API_CONTRACTS.md)."""
        if role_of(request.user) == ROLE_ADMIN:
            return True
        if cat.user_id == request.user.id:
            return True
        publication = getattr(cat, "publication", None)
        return publication is not None and publication.visibility == Publication.Visibility.PUBLIC

    def patch(self, request, pk):
        cat = self._get_cat(pk)
        self.check_object_permissions(request, cat)
        configuration = request.data.get("configuration", cat.configuration)
        name = request.data.get("name", cat.name)
        updated = update_cat(cat, configuration, name=name)
        return Response(CatSerializer(updated).data)

    def delete(self, request, pk):
        cat = self._get_cat(pk)
        self.check_object_permissions(request, cat)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

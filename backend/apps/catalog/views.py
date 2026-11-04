from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import CatalogOption, Pose
from .serializers import CatalogOptionSerializer, PoseSerializer


class CatalogListView(ListAPIView):
    """Opciones activas agrupadas por categoría, más las poses (P08 · `/api/catalog/`)."""

    serializer_class = CatalogOptionSerializer
    rbac_public = True

    def get_queryset(self):
        return CatalogOption.objects.filter(is_active=True).order_by("category", "z_order", "code")

    def list(self, request, *args, **kwargs):
        options = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True).data
        categories: dict[str, list] = {}
        for option in options:
            categories.setdefault(option["category"], []).append(option)
        return Response({"schema_version": 1, "categories": categories})


class PoseListView(ListAPIView):
    serializer_class = PoseSerializer
    rbac_public = True
    queryset = Pose.objects.filter(is_active=True)

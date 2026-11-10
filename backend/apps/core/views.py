from django.db import connection
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers


class HealthSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["ok", "degraded"])
    database = serializers.ChoiceField(choices=["up", "down"])
    engine = serializers.CharField(help_text="Motor de base de datos en uso (mysql o sqlite).")


@extend_schema(responses=HealthSerializer)
@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    """Verificación de disponibilidad (03_ARCHITECTURE.md · Documentación de la API)."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        database = "up"
    except Exception:
        database = "down"

    return Response({"status": "ok" if database == "up" else "degraded", "database": database, "engine": connection.vendor})

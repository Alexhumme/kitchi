from rest_framework import serializers

from .models import Cat


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ["id", "name", "configuration", "schema_version", "created_at", "updated_at"]
        read_only_fields = ["id", "schema_version", "created_at", "updated_at"]

    def validate_configuration(self, value):
        # La validación contra el catálogo vive en apps.catalog.services y se
        # aplica en la vista, donde se conoce al usuario que solicita.
        if not isinstance(value, dict):
            raise serializers.ValidationError("La configuración debe ser un objeto JSON.")
        return value

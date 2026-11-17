from rest_framework import serializers

from apps.cats.models import Cat

from .models import Publication


class PublicationCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ("id", "name", "configuration", "created_at")


class PublicationReadSerializer(serializers.ModelSerializer):
    """Lectura de una publicación: autor público y gato embebido (P18)."""

    author = serializers.CharField(source="user.username", read_only=True)
    cat = PublicationCatSerializer(read_only=True)

    class Meta:
        model = Publication
        fields = (
            "id",
            "title",
            "description",
            "visibility",
            "author",
            "cat",
            "created_at",
            "updated_at",
        )


class PublicationWriteSerializer(serializers.Serializer):
    """Entrada para publicar: el gato ya debe existir y ser del autor."""

    cat_id = serializers.IntegerField(min_value=1)
    title = serializers.CharField(max_length=120)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True, default="")
    visibility = serializers.ChoiceField(
        choices=Publication.Visibility.choices, default=Publication.Visibility.PUBLIC
    )

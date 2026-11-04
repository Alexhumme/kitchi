from django.db import models

from apps.cats.models import Cat


class PublicationQuerySet(models.QuerySet):
    def visible_for(self, user) -> "PublicationQuerySet":
        """El hub muestra lo público; el autor además ve sus borradores privados."""
        if user is not None and user.is_authenticated:
            return self.filter(models.Q(visibility=Publication.Visibility.PUBLIC) | models.Q(user=user))
        return self.filter(visibility=Publication.Visibility.PUBLIC)


class Publication(models.Model):
    """Creación compartida en el hub; entidad separada del gato (04_DATA_MODEL.md)."""

    class Visibility(models.TextChoices):
        PUBLIC = "public", "Pública"
        PRIVATE = "private", "Privada"

    cat = models.OneToOneField(Cat, on_delete=models.CASCADE, related_name="publication")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="publications")
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, max_length=500)
    visibility = models.CharField(
        max_length=12, choices=Visibility.choices, default=Visibility.PUBLIC, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PublicationQuerySet.as_manager()

    class Meta:
        db_table = "publications"
        verbose_name = "publicación"
        verbose_name_plural = "publicaciones"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"], name="pubs_user_created_idx"),
            models.Index(fields=["visibility", "created_at"], name="pubs_visibility_created_idx"),
        ]

    def __str__(self):
        return f"{self.title} · {self.user.username}"

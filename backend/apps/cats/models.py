from django.contrib.auth.models import User
from django.db import models

CONFIG_SCHEMA_VERSION = 1


class Cat(models.Model):
    """Personaje guardado; su apariencia se reconstruye desde `configuration` (ADR-002)."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cats")
    name = models.CharField(max_length=80)
    configuration = models.JSONField(default=dict, help_text="Documento validado contra el catálogo.")
    schema_version = models.PositiveSmallIntegerField(default=CONFIG_SCHEMA_VERSION)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cats"
        verbose_name = "gato"
        verbose_name_plural = "gatos"
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_cat_name_per_user"),
        ]
        indexes = [models.Index(fields=["user", "created_at"], name="cats_user_created_idx")]

    def __str__(self):
        return f"{self.name} · {self.user.username}"

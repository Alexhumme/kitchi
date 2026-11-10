from django.db import models


class CatalogOption(models.Model):
    """Una opción del editor, validada contra `assets/catalog.json` (06_DESIGN_SYSTEM.md)."""

    CATEGORY_CHOICES = [
        ("fur", "Pelaje"),
        ("eyes", "Ojos"),
        ("hair", "Cabello"),
        ("top", "Parte superior"),
        ("bottom", "Parte inferior"),
        ("accessory", "Accesorio"),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    code = models.CharField(max_length=60, help_text="Identificador estable enviado por la interfaz.")
    label = models.CharField(max_length=80)
    asset_path = models.CharField(max_length=255, blank=True)
    z_order = models.PositiveSmallIntegerField(default=0, help_text="Orden explícito de composición.")
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "catalog_options"
        verbose_name = "opción del catálogo"
        verbose_name_plural = "opciones del catálogo"
        constraints = [
            models.UniqueConstraint(fields=["category", "code"], name="unique_option_per_category"),
        ]
        indexes = [models.Index(fields=["category", "is_active"])]

    def __str__(self):
        return f"{self.category}:{self.code}"


class Pose(models.Model):
    """Pose del catálogo de stickers; el paquete completo usa las activas."""

    code = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=80)
    asset_path = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "poses"
        verbose_name = "pose"
        verbose_name_plural = "poses"
        ordering = ["code"]

    def __str__(self):
        return self.code

    @classmethod
    def active_codes(cls):
        return list(cls.objects.filter(is_active=True).values_list("code", flat=True))

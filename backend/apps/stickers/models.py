from django.db import models

from apps.core.models import STATUS_COMPLETED, StatusMixin
from apps.catalog.models import Pose
from apps.cats.models import Cat


class StickerPack(StatusMixin):
    """Paquete de seis stickers generados a partir de un gato guardado."""

    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name="sticker_packs")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "sticker_packs"
        verbose_name = "paquete de stickers"
        verbose_name_plural = "paquetes de stickers"
        indexes = [models.Index(fields=["cat", "created_at"], name="packs_cat_created_idx")]

    def __str__(self):
        return f"Paquete {self.pk} · {self.cat.name} · {self.status}"

    @property
    def is_complete(self) -> bool:
        expected = Pose.objects.filter(is_active=True).count()
        return expected > 0 and self.stickers.filter(status=STATUS_COMPLETED).count() == expected


class Sticker(models.Model):
    """Un PNG exportado para una pose concreta del paquete."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        COMPLETED = "completed", "Completado"
        FAILED = "failed", "Fallido"

    pack = models.ForeignKey(StickerPack, on_delete=models.CASCADE, related_name="stickers")
    pose = models.ForeignKey(Pose, on_delete=models.PROTECT, related_name="stickers")
    file_path = models.CharField(max_length=255, blank=True, help_text="Ruta relativa a storage/.")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True)
    error_code = models.CharField(max_length=64, blank=True)

    class Meta:
        db_table = "stickers"
        verbose_name = "sticker"
        verbose_name_plural = "stickers"
        constraints = [
            models.UniqueConstraint(fields=["pack", "pose"], name="one_sticker_per_pose_per_pack"),
        ]
        indexes = [models.Index(fields=["pack", "status"], name="stickers_pack_status_idx")]

    def __str__(self):
        return f"{self.pack_id} · {self.pose.code} · {self.status}"

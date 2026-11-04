from django.conf import settings
from django.db import models

from apps.core.models import (
    STATUS_COMPLETED,
    STATUS_FAILED,
    STATUS_RUNNING,
    StatusMixin,
)


class GenerationJob(StatusMixin):
    """Registro de un trabajo de IA o de composición, con estados validados."""

    class JobType(models.TextChoices):
        PHOTO_TO_CHIBI = "photo_to_chibi", "Fotografía a chibi"
        STICKER_PACK = "sticker_pack", "Paquete de stickers"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="generation_jobs")
    job_type = models.CharField(max_length=32, choices=JobType.choices, db_index=True)
    input_payload = models.JSONField(default=dict, help_text="Entrada normalizada; sin datos personales en bruto.")
    result = models.JSONField(default=dict, blank=True)
    provider = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "generation_jobs"
        verbose_name = "trabajo de generación"
        verbose_name_plural = "trabajos de generación"
        indexes = [models.Index(fields=["user", "created_at"], name="jobs_user_created_idx")]

    def __str__(self):
        return f"{self.job_type} · {self.user.username} · {self.status}"

    def mark_started(self, when):
        self.transition_to(STATUS_RUNNING)
        self.started_at = when
        self.save(update_fields=["status", "started_at", "error_code"])

    def mark_completed(self, when, result=None):
        self.transition_to(STATUS_COMPLETED)
        self.completed_at = when
        if result is not None:
            self.result = result
        self.save(update_fields=["status", "completed_at", "result", "error_code"])

    def mark_failed(self, error_code: str):
        self.transition_to(STATUS_FAILED, error_code=error_code)
        self.completed_at = None
        self.save(update_fields=["status", "error_code", "completed_at"])

    @property
    def is_ai_available(self) -> bool:
        return settings.AI_PROVIDER != "none" and bool(settings.AI_API_KEY)

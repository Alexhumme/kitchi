from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .permissions import ROLE_ADMIN, ROLE_MEMBER


class UserProfile(models.Model):
    """Extensión de User para RBAC y plan del usuario (04_DATA_MODEL.md · users)."""

    class Role(models.TextChoices):
        MEMBER = ROLE_MEMBER, "Miembro"
        ADMIN = ROLE_ADMIN, "Administrador"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.MEMBER, db_index=True)
    premium = models.BooleanField(
        default=False,
        help_text="Plan simulado del MVP (02_REQUIREMENTS.md); no implica pago real.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_profiles"
        verbose_name = "perfil de usuario"
        verbose_name_plural = "perfiles de usuario"

    def __str__(self):
        return f"{self.user.username} · {self.get_role_display()}"


@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

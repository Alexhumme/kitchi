"""Paquetes y stickers: el estado solo cambia con las acciones que respetan la máquina de estados."""

from django.contrib import admin, messages
from django.utils import timezone

from apps.catalog.models import Pose
from apps.core.models import (
    STATUS_COMPLETED,
    STATUS_FAILED,
    STATUS_PENDING,
    STATUS_RUNNING,
)

from .models import Sticker, StickerPack


class StickerInline(admin.TabularInline):
    model = Sticker
    extra = 0
    autocomplete_fields = ("pose",)


@admin.register(StickerPack)
class StickerPackAdmin(admin.ModelAdmin):
    list_display = ("id", "cat", "owner", "status", "ready_stickers", "error_code", "created_at", "completed_at")
    list_filter = ("status", "cat__user")
    search_fields = ("cat__name", "cat__user__username")
    autocomplete_fields = ("cat",)
    readonly_fields = ("status", "error_code", "created_at", "completed_at", "is_complete")
    fieldsets = (
        ("Paquete", {"fields": ("cat", "status", "error_code")}),
        ("Resultado", {"fields": ("is_complete", "created_at", "completed_at")}),
    )
    inlines = (StickerInline,)
    actions = ("poner_en_ejecucion", "marcar_completados", "marcar_fallidos", "volver_a_la_cola")

    @admin.display(description="Dueño")
    def owner(self, obj):
        return obj.cat.user.username

    @admin.display(description="Stickers listos")
    def ready_stickers(self, obj):
        expected = Pose.objects.filter(is_active=True).count()
        return f"{obj.stickers.filter(status=Sticker.Status.COMPLETED).count()} de {expected}"

    @admin.action(description="Pasar a en ejecución")
    def poner_en_ejecucion(self, request, queryset):
        self._transition(request, queryset, STATUS_RUNNING)

    @admin.action(description="Marcar como completados")
    def marcar_completados(self, request, queryset):
        self._transition(request, queryset, STATUS_COMPLETED)

    @admin.action(description="Marcar como fallidos")
    def marcar_fallidos(self, request, queryset):
        self._transition(request, queryset, STATUS_FAILED)

    @admin.action(description="Devolver a la cola (pendiente)")
    def volver_a_la_cola(self, request, queryset):
        self._transition(request, queryset, STATUS_PENDING)

    def _transition(self, request, queryset, new_status):
        """Aplica la transición modelo a modelo; las ilegales se informan, no se fuerzan."""
        changed = 0
        for pack in queryset:
            try:
                pack.transition_to(new_status)
            except ValueError:
                continue
            if new_status == STATUS_COMPLETED:
                pack.completed_at = timezone.now()
            pack.save(update_fields=["status", "error_code", "completed_at"])
            changed += 1
        skipped = queryset.count() - changed
        if changed:
            self.message_user(request, f"{changed} paquetes actualizados a «{new_status}».", messages.SUCCESS)
        if skipped:
            self.message_user(
                request,
                f"{skipped} paquetes omitidos: su estado actual no permite esa transición.",
                messages.WARNING,
            )


@admin.register(Sticker)
class StickerAdmin(admin.ModelAdmin):
    list_display = ("pack", "pose", "status", "error_code", "file_path")
    list_filter = ("status", "pose")
    search_fields = ("file_path", "pack__cat__name", "pack__cat__user__username")
    autocomplete_fields = ("pack", "pose")

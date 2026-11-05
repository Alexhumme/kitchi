"""Trabajos de generación: el estado se cambia con los métodos del modelo, nunca a mano."""

from django.contrib import admin, messages
from django.utils import timezone

from apps.core.models import STATUS_PENDING

from .models import GenerationJob


def _start(job):
    job.mark_started(timezone.now())


def _complete(job):
    job.mark_completed(timezone.now())


def _fail(job):
    job.mark_failed("ADMIN_MANUAL")


def _retry(job):
    job.transition_to(STATUS_PENDING)
    job.save(update_fields=["status", "error_code"])


@admin.register(GenerationJob)
class GenerationJobAdmin(admin.ModelAdmin):
    list_display = ("id", "job_type", "user", "status", "error_code", "provider", "created_at", "completed_at")
    list_filter = ("status", "job_type", "provider")
    search_fields = ("user__username", "provider")
    autocomplete_fields = ("user",)
    readonly_fields = ("status", "error_code", "created_at", "started_at", "completed_at")
    fieldsets = (
        ("Trabajo", {"fields": ("user", "job_type", "provider", "input_payload", "result")}),
        ("Estado", {"fields": ("status", "error_code")}),
        ("Fechas", {"fields": ("created_at", "started_at", "completed_at")}),
    )
    date_hierarchy = "created_at"
    actions = ("poner_en_ejecucion", "marcar_completados", "marcar_fallidos", "reintentar")

    @admin.action(description="Pasar a en ejecución")
    def poner_en_ejecucion(self, request, queryset):
        self._apply(request, queryset, _start)

    @admin.action(description="Marcar como completados")
    def marcar_completados(self, request, queryset):
        self._apply(request, queryset, _complete)

    @admin.action(description="Marcar como fallidos")
    def marcar_fallidos(self, request, queryset):
        self._apply(request, queryset, _fail)

    @admin.action(description="Devolver a la cola (pendiente)")
    def reintentar(self, request, queryset):
        self._apply(request, queryset, _retry)

    def _apply(self, request, queryset, operation):
        """Ejecuta el método de ciclo de vida; las transiciones ilegales se informan."""
        changed = 0
        for job in queryset:
            try:
                operation(job)
            except ValueError:
                continue
            changed += 1
        if changed:
            self.message_user(request, f"{changed} trabajos actualizados.", messages.SUCCESS)
        skipped = queryset.count() - changed
        if skipped:
            self.message_user(
                request,
                f"{skipped} trabajos omitidos: su estado actual no permite esa transición.",
                messages.WARNING,
            )

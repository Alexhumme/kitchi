"""Publicaciones del hub: visibilidad editable por el equipo administrador."""

from django.contrib import admin, messages

from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "cat", "visibility", "created_at", "updated_at")
    list_filter = ("visibility", "created_at")
    search_fields = ("title", "description", "user__username", "cat__name")
    autocomplete_fields = ("cat", "user")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    actions = ("hacer_publicas", "hacer_privadas")

    @admin.action(description="Publicar en el hub")
    def hacer_publicas(self, request, queryset):
        updated = queryset.update(visibility=Publication.Visibility.PUBLIC)
        self.message_user(request, f"{updated} publicaciones visibles en el hub.", messages.SUCCESS)

    @admin.action(description="Retirar del hub (privada)")
    def hacer_privadas(self, request, queryset):
        updated = queryset.update(visibility=Publication.Visibility.PRIVATE)
        self.message_user(request, f"{updated} publicaciones ocultas del hub.", messages.WARNING)

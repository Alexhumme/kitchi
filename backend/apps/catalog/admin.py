"""Gestión del catálogo de opciones y de las poses desde la consola de administración."""

from django.contrib import admin, messages

from apps.stickers.models import Sticker

from .models import CatalogOption, Pose


@admin.register(CatalogOption)
class CatalogOptionAdmin(admin.ModelAdmin):
    list_display = ("code", "category", "label", "z_order", "asset_path", "is_premium", "is_active")
    list_filter = ("category", "is_premium", "is_active")
    search_fields = ("code", "label", "asset_path")
    list_editable = ("z_order", "is_premium", "is_active")
    list_per_page = 50
    ordering = ("category", "z_order", "code")
    actions = ("activar_opciones", "desactivar_opciones")

    @admin.action(description="Activar las opciones seleccionadas")
    def activar_opciones(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} opciones activadas.", messages.SUCCESS)

    @admin.action(description="Desactivar las opciones seleccionadas")
    def desactivar_opciones(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} opciones desactivadas.", messages.WARNING)


@admin.register(Pose)
class PoseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "asset_path", "generated_stickers", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name", "asset_path")
    list_editable = ("is_active",)
    actions = ("activar_poses", "desactivar_poses")

    @admin.display(description="Stickers generados")
    def generated_stickers(self, obj):
        return obj.stickers.exclude(status=Sticker.Status.PENDING).count()

    @admin.action(description="Activar las poses seleccionadas")
    def activar_poses(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} poses activadas.", messages.SUCCESS)

    @admin.action(description="Desactivar las poses seleccionadas")
    def desactivar_poses(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f"{updated} poses desactivadas. Los paquetes siguientes usarán solo las poses activas.",
            messages.WARNING,
        )

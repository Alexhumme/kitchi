"""Los personajes se gestionan con la misma validación de catálogo que la API.

Reutilizar `validate_configuration` evita que la consola acepte documentos que
`/api/cats/` rechazaría (AGENTS.md: no duplicar lógica de negocio).
"""

from django import forms
from django.contrib import admin

from apps.catalog.services import validate_configuration
from apps.core.errors import APIError

from .models import CONFIG_SCHEMA_VERSION, Cat


class CatAdminForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = "__all__"

    def clean_configuration(self):
        configuration = self.cleaned_data["configuration"]
        user = self.cleaned_data.get("user") or getattr(self.instance, "user", None)
        try:
            return validate_configuration(configuration, user=user)
        except APIError as error:
            problems = [error.message]
            for key, detail in error.details.get("campos", {}).items():
                problems.append(f"«{key}»: {detail}")
            raise forms.ValidationError(problems) from error


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    form = CatAdminForm
    list_display = ("name", "user", "schema_version", "publication_state", "created_at", "updated_at")
    list_filter = ("schema_version", "publication__visibility")
    search_fields = ("name", "user__username")
    autocomplete_fields = ("user",)
    readonly_fields = ("schema_version", "created_at", "updated_at")
    date_hierarchy = "created_at"

    @admin.display(description="Publicación")
    def publication_state(self, obj):
        publication = getattr(obj, "publication", None)
        if publication is None:
            return "Sin publicar"
        return publication.get_visibility_display()

    def save_model(self, request, obj, form, change):
        obj.schema_version = obj.configuration.get("schema_version", CONFIG_SCHEMA_VERSION)
        super().save_model(request, obj, form, change)

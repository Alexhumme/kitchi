from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile

# `django.contrib.auth.admin` ya registra `User`; se sustituye por la versión con perfil.
admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = "Perfil"
    verbose_name_plural = "Perfil y permisos"


@admin.register(User)
class KitchiUserAdmin(UserAdmin):
    """El perfil se edita junto al usuario: el rol RBAC no vive en otra pantalla."""

    inlines = (UserProfileInline,)
    list_display = ("username", "email", "role", "premium", "is_staff", "date_joined")
    list_filter = ("profile__role", "profile__premium", "is_staff")
    search_fields = ("username", "email")

    @admin.display(description="Rol", ordering="profile__role")
    def role(self, obj):
        return obj.profile.role

    @admin.display(description="Plan", boolean=True, ordering="profile__premium")
    def premium(self, obj):
        return obj.profile.premium


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "premium", "updated_at")
    list_filter = ("role", "premium")
    search_fields = ("user__username", "user__email")
    autocomplete_fields = ("user",)

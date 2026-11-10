"""Marca la consola de administración con el nombre del proyecto."""

from django.contrib import admin

admin.site.site_header = "Administración de Kitchi Studio"
admin.site.site_title = "Kitchi Studio"
admin.site.index_title = "Cuentas, catálogo, personajes y trabajos"

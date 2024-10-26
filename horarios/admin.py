from django.contrib import admin

# Register your models here.
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Seccion

@admin.register(Seccion)
class SeccionAdmin(ImportExportModelAdmin):
    list_display = ('curso', 'nombre', 'cupos_totales', 'semestre')

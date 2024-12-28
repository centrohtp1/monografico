from django.contrib import admin

# Register your models here.
# anio_escolar/admin.py
from django.contrib import admin
from .models import AnioEscolar

@admin.register(AnioEscolar)
class AnioEscolarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)

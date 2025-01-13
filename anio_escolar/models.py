# anio_escolar/models.py
from django.db import models
from django.utils import timezone

class AnioEscolar(models.Model):
    nombre = models.CharField(max_length=10, unique=True, verbose_name="Año Escolar")  # Ej: 2024-2025
    activo = models.BooleanField(default=True, verbose_name="Activo")  # Para marcar el año escolar activo
   # fecha_ingreso = models.DateField(default=timezone.now) 
    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['-nombre']  # Ordenar por el año más reciente primero
        verbose_name = "Año Escolar"
        verbose_name_plural = "Años Escolares"

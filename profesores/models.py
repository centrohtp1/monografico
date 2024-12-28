from django.db import models
from django.utils.timezone import now 

class Profesor(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_contratacion = models.DateField(default=now )

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.especialidad}"

from datetime import timezone
from django.db import models
from estudiantes.models import Estudiante  # Importa desde la app correcta
from profesores.models import Profesor    # Importa desde la app correcta
from django.utils.timezone import now 

class Curso(models.Model):
    nombre = models.CharField(max_length=200, unique=True)  # Campo único para el nombre del curso
    descripcion = models.TextField()
    profesores = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateField(default=now)

    def __str__(self):
        return self.nombre

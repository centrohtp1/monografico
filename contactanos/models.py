from django.db import models

# Create your models here.
from django.db import models

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return f'Contacto de {self.nombre} ({self.correo_electronico})'

from django.db import models

class Registration(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre Completo")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    anio = models.PositiveIntegerField(verbose_name="Edad")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Registro"
        verbose_name_plural = "Registros"

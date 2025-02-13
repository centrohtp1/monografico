from django.db import models
from estudiantes.models import Estudiante
from Cursos.models import Curso
from profesores.models import Profesor

class Seccion(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_termino = models.DateField(null=True, blank=True)
    estudiantes = models.ManyToManyField(Estudiante, related_name='secciones')
    pagado = models.BooleanField(default=False)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, null=True, blank=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def puede_agregar_estudiante(self):
        return self.estudiantes.count() < 25

class SeccionEstudiante(models.Model):
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    nota2 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    nota3 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    nota4 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    promedio = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, editable=False)

    def calcular_promedio(self):
        notas = [self.nota, self.nota2, self.nota3, self.nota4]
        notas_validas = [notase for notase in notas if notase is not None]
        return sum(notas_validas) / len(notas_validas) if notas_validas else None

    def save(self, *args, **kwargs):
        self.promedio = self.calcular_promedio()
        super().save(*args, **kwargs)

    @property
    def estado(self):
        if self.promedio is not None:
            if self.promedio >= 75:
                return 'Promovido'
            elif 55 <= self.promedio < 75:
                return 'Recuperación Pedagógica'
            else:
                return 'Reprobado'
        return 'Sin Nota'

    def __str__(self):
        return f"{self.estudiante} - {self.seccion} - Promedio: {self.promedio} - Estado: {self.estado}"

    class Meta:
        verbose_name = "Sección Estudiante"
        verbose_name_plural = "Sección Estudiantes"

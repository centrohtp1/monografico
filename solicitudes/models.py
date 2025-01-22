from django.db import models

class Registration(models.Model):
    # Opciones para el campo "curso_a_solicitar"
    CURSOS = [
        ('HSC', 'Habilidades Sociales y Comunicación'),
        ('DLC', 'Desarrollo del Lenguaje y la Comunicación'),
        ('ECA', 'Estimulación Cognitiva y Aprendizaje'),
        ('HVD', 'Habilidades para la Vida Diaria'),
        ('TA', 'Tecnología Asistiva'),
        ('EAC', 'Expresión Artística y Creatividad'),
        ('PEE', 'Preparación para la Inclusión Escolar'),
        ('IBA', 'Informática Básica Adaptada'),
        ('EMC', 'Estrategias de Manejo Conductual'),
        ('CE', 'Comunicación Efectiva con Niños con Necesidades Especiales'),
        ('AC', 'Adaptaciones Curriculares'),
        ('IT', 'Intervención Temprana'),
        ('CNE', 'Conociendo las Necesidades Educativas Especiales'),
    ]
    
    nombre = models.CharField(max_length=255, verbose_name="Nombre Completo")
    email = models.EmailField(verbose_name="Correo Electrónico")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    anio = models.PositiveIntegerField(verbose_name="Edad")
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    # Nuevo campo curso_a_solicitar
    curso_a_solicitar = models.CharField(
        max_length=3, 
        choices=CURSOS, 
        verbose_name="Curso a Solicitar", 
        default='HSC'  # Valor predeterminado para las filas existentes
    )


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Registro"
        verbose_name_plural = "Registros"

# estudiantes/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from anio_escolar.models import AnioEscolar
from django.core.validators import RegexValidator

class Estudiante(models.Model):
    Ciudades = [
  
    ('A', 'Azua'),
    ('BH', 'Bahoruco'),
    ('BA', 'Barahona'),
    ('D', 'Dajabón'),
    ('DN', 'Distrito Nacional'),
    ('DU', 'Duarte'),
    ('EP', 'Elías Piña'),
    ('ES', 'El Seibo'),
    ('E', 'Espaillat'),
    ('H', 'Hato Mayor'),
    ('HM', 'Hermanas Mirabal'),
    ('I', 'Independencia'),
    ('LA', 'La Altagracia'),
    ('LR', 'La Romana'),
    ('LV', 'La Vega'),
    ('MTS', 'María Trinidad Sánchez'),
    ('MN', 'Monseñor Nouel'),
    ('MC', 'Monte Cristi'),
    ('MT', 'Monte Plata'),
    ('P', 'Pedernales'),
    ('PR', 'Peravia'),
    ('PP', 'Puerto Plata'),
    ('S', 'Samaná'),
    ('SR', 'Sánchez Ramírez'),
    ('SC', 'San Cristóbal'),
    ('SJO', 'San José de Ocoa'),
    ('SJ', 'San Juan'),
    ('SPM', 'San Pedro de Macorís'),
    ('SA', 'Santiago'),
    ('SAR', 'Santiago Rodríguez'),
    ('SD', 'Santo Domingo'),
    ('V', 'Valverde'),
  
]
    
    
    Tipo = [
    ('A','Activo'),
    ('I','Inactivo'),
  
  
]
 solo_letras = RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', 'Este campo solo puede contener letras.')



    # Datos personales
    nombre = models.CharField(max_length=50, verbose_name= "Nombres",validators=[solo_letras] )
    apellido = models.CharField(max_length=50, verbose_name="Aplleidos",validators=[solo_letras] )
    fecha_nacimiento = models.DateField()
    genero = models.CharField(
        max_length=10,
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        default='O'
    )
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    # Dirección
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(choices=Ciudades, max_length=50)
    

    estado = models.CharField(choices=Tipo,max_length=50)
   

    # Información académica
    matricula = models.CharField(max_length=20, unique=True)
    fecha_ingreso = models.DateField(default=timezone.now) 
   
    grado = models.CharField(max_length=20)  # Ej: 1° de Primaria, 2° de Secundaria
  
     
    anio_escolar = models.ForeignKey(
        AnioEscolar,
        on_delete=models.PROTECT,  # Evitar eliminar un año escolar en uso
        verbose_name="Año Escolar"
    )



    # Métodos especiales
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.matricula}"

    def save(self, *args, **kwargs):
        if not self.matricula:
            # Obtener las primeras letras del nombre y apellido
            iniciales = f"{self.nombre[0].lower()}{self.apellido[0].lower()}"

            # Obtener el año actual
            anio_actual = timezone.now().year

            # Contar las matrículas existentes que comienzan con las iniciales y el año
            conteo = Estudiante.objects.filter(matricula__startswith=f"{iniciales}-{anio_actual}-").count()

            # Incrementar el contador y generar la matrícula
            contador = conteo + 1
            self.matricula = f"{iniciales}-{anio_actual}-{str(contador).zfill(4)}"  # Usar zfill para asegurar un formato de 4 dígitos

        super().save(*args, **kwargs)


    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

 

# Generated by Django 5.1.2 on 2024-12-21 02:37

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudiantes', '0005_alter_estudiante_anio_escolar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='apellido',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+$', 'Este campo solo puede contener letras.')], verbose_name='Aplleidos'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='fecha_ingreso',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='nombre',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+$', 'Este campo solo puede contener letras.')], verbose_name='Nombres'),
        ),
    ]

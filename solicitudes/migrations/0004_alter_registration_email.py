# Generated by Django 5.1.2 on 2025-01-22 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0003_registration_curso_a_solicitar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Correo Electrónico'),
        ),
    ]

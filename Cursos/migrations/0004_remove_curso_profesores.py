# Generated by Django 5.1.2 on 2025-01-22 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cursos', '0003_alter_curso_fecha_creacion_alter_curso_nombre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='profesores',
        ),
    ]

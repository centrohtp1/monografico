# Generated by Django 5.1.2 on 2025-01-14 04:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anio_escolar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='anioescolar',
            name='fecha_ingreso',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

# Generated by Django 5.1.2 on 2025-01-22 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]

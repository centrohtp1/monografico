# Generated by Django 5.1.2 on 2024-12-20 15:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudiantes', '0003_alter_estudiante_anio_escolar'),
        ('facturacion', '0002_initial'),
        ('secciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuentaporcobrar',
            name='estudiante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='estudiantes.estudiante'),
        ),
        migrations.AlterField(
            model_name='cuentaporcobrar',
            name='seccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='secciones.seccion'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='cuenta_por_cobrar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='facturas', to='facturacion.cuentaporcobrar'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='estudiante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='estudiantes.estudiante'),
        ),
        migrations.AlterField(
            model_name='tarifa',
            name='secciones_tarifa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='secciones.seccion'),
        ),
    ]

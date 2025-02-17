# Generated by Django 5.1.2 on 2024-11-15 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuariohtp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('identificacion', models.IntegerField(blank=True, max_length=13, null=True, unique=True)),
                ('nombre', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombres')),
                ('apellido', models.CharField(blank=True, max_length=200, null=True, verbose_name='Apellidos')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Nombre de usuario')),
                ('telefono', models.CharField(blank=True, max_length=12, null=True)),
                ('direccion', models.CharField(blank=True, max_length=128, null=True)),
                ('imagen', models.ImageField(default='perfil/avatar.png', max_length=200, upload_to='perfil/', verbose_name='Imagen de Perfil')),
                ('usuario_activo', models.BooleanField(default=True)),
                ('usuario_administrador', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

# notificaciones/serializers.py
from rest_framework import serializers

from secciones.models import Seccion
from .models import Notificacion

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'titulo', 'mensaje', 'seccion', 'fecha_creacion', 'leido']

class SeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seccion
        fields = ['id', 'nombre', 'grado', 'fecha_termino']
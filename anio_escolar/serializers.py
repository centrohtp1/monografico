# anio_escolar/serializers.py
from rest_framework import serializers
from .models import AnioEscolar

class AnioEscolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnioEscolar
        fields = ['id', 'nombre', 'activo']  # Incluye todos los campos que deseas exponer

    def validate_nombre(self, value):
        """Validar el formato del año escolar"""
        if not value or '-' not in value:
            raise serializers.ValidationError("El nombre del año escolar debe estar en el formato 'YYYY-YYYY'.")
        return value

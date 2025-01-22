# estudiantes/serializers.py
from rest_framework import serializers
from .models import Estudiante
import re


class EstudianteSerializer(serializers.ModelSerializer):
    matricula = serializers.ReadOnlyField()  # Esto hará que 'matricula' sea solo lectura
    
    # Validación personalizada para correo único
    def validate_email(self, value):
        # Obtener el estudiante que se está actualizando, si hay uno
        estudiante = self.instance
        
        # Si el correo electrónico ha cambiado, se realiza la validación
        if estudiante and value != estudiante.email:
            # Verificar si el correo electrónico ya existe en otro estudiante
            if Estudiante.objects.filter(email=value).exists():
                raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        
        return value

    # Validación personalizada para el campo nombre (letras, acentos y espacios)
    def validate_nombre(self, value):
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras, incluyendo acentos y espacios.")
        return value

    # Validación personalizada para el campo apellido (letras, acentos y espacios)
    def validate_apellido(self, value):
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', value):
            raise serializers.ValidationError("El apellido solo puede contener letras, incluyendo acentos y espacios.")
        return value

    class Meta:
        model = Estudiante
        fields = '__all__'  # Incluye todos los campos del modelo

# estudiantes/serializers.py
from rest_framework import serializers
from .models import Estudiante

class EstudianteSerializer(serializers.ModelSerializer):
    matricula = serializers.ReadOnlyField()  # Esto hará que 'matricula' sea solo lectura
    
    # Validación personalizada para correo único
    def validate_email(self, value):
        # Verificar si el correo electrónico ya existe
        if Estudiante.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value

    # Validación personalizada para el campo nombre (solo letras y sin números)
    def validate_nombre(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("El nombre solo puede contener letras.")
        return value

    # Validación personalizada para el campo apellido (solo letras y sin números)
    def validate_apellido(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("El apellido solo puede contener letras.")
        return value

    class Meta:
        model = Estudiante
        fields = '__all__'  # Incluye todos los campos del modelo

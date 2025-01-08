from rest_framework import serializers
from .models import Estudiante

class EstudianteSerializer(serializers.ModelSerializer):
    matricula = serializers.ReadOnlyField()  # Esto hará que 'matricula' sea solo lectura
    
    class Meta:
        model = Estudiante
        fields = '__all__'  # Incluye todos los campos del modelo

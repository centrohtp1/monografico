# estudiantes/serializers.py
 #  fields = '__all__'
from rest_framework import serializers
from .models import Estudiante

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        exclude = ['matricula']
     

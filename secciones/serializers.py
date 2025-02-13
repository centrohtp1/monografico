# secciones/serializers.py
from rest_framework import serializers

from Cursos.models import Curso
from profesores.models import Profesor
from .models import Seccion, SeccionEstudiante
from estudiantes.models import Estudiante

class SeccionSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Seccion
        fields = '__all__'  # Ajusta los campos según sea necesario

class SeccionSerializer(serializers.ModelSerializer):
    # Aquí agregamos el campo profesor
    
    class Meta:
        model = Seccion
        fields = ['nombre', 'fecha_inicio', 'fecha_termino', 'curso', 'profesor', 'pagado']  # Ajusta los campos según sea necesario

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ['id', 'nombre']  # Ajusta los campos según sea necesario

class SeccionEstudianteSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer()

    class Meta:
        model = SeccionEstudiante
        fields = ['estudiante', 'nota1', 'nota2', 'nota3', 'nota4', 'promedio']  # Ajusta los campos según sea necesario

    def update(self, instance, validated_data):
        # Actualiza las notas
        instance.nota = validated_data.get('nota1', instance.nota)
        instance.nota2 = validated_data.get('nota2', instance.nota2)
        instance.nota3 = validated_data.get('nota3', instance.nota3)
        instance.nota4 = validated_data.get('nota4', instance.nota4)

        # Calcular el promedio basado en las notas
        instance.promedio = (instance.nota + instance.nota2 + instance.nota3 + instance.nota4) / 4
        instance.save()
        return instance




# estudiantes/views.py
from rest_framework import viewsets
from .models import Estudiante
from .serializers import EstudianteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser
class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    parser_classes = [JSONParser, FormParser]
   # permission_classes = [IsAuthenticated]


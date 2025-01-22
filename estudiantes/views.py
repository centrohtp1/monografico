# estudiantes/views.py
#from rest_framework import viewsets
#from .models import Estudiante
#from .serializers import EstudianteSerializer
#from rest_framework.permissions import IsAuthenticated
#from rest_framework.parsers import JSONParser, FormParser
#class EstudianteViewSet(viewsets.ModelViewSet):
 #   queryset = Estudiante.objects.all()
  #  serializer_class = EstudianteSerializer
#    parser_classes = [JSONParser, FormParser]
   # permission_classes = [IsAuthenticated]

# estudiantes/views.py
from rest_framework import viewsets
from .models import Estudiante
from .serializers import EstudianteSerializer
from rest_framework.response import Response
from rest_framework import status

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Si es válido, se guarda el estudiante
            serializer.save()
            return Response({"success": True, "message": "Estudiante creado exitosamente."}, status=status.HTTP_201_CREATED)
        else:
            # Si hay errores de validación, se devuelven los errores detallados
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # Permite soportar actualizaciones parciales (PATCH)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Estudiante actualizado exitosamente."}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": True, "message": "Estudiante eliminado exitosamente."}, status=status.HTTP_200_OK)
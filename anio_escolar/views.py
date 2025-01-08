from django.shortcuts import render

# Create your views here.
# anio_escolar/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AnioEscolar
from .serializers import AnioEscolarSerializer

class AnioEscolarCRUDView(APIView):
      def get(self, request, pk=None):
        """Listar todos los años escolares o uno en específico"""
        if pk is None:
            # Obtener todos los años escolares
            anios = AnioEscolar.objects.all()
            serializer = AnioEscolarSerializer(anios, many=True)
            return Response({
                "message": "Lista de años escolares obtenida con éxito.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            # Obtener un solo año escolar por pk
            try:
                anio = AnioEscolar.objects.get(pk=pk)
                serializer = AnioEscolarSerializer(anio)
                return Response({
                    "message": "Año escolar encontrado con éxito.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            except AnioEscolar.DoesNotExist:
                return Response({
                    "message": "Año escolar no encontrado."
                }, status=status.HTTP_404_NOT_FOUND)

        def post(self, request):
            """Crear un nuevo año escolar"""
            serializer = AnioEscolarSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Año escolar creado con éxito.",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                "message": "Error al crear el año escolar.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        def put(self, request, pk):
            """Actualizar un año escolar existente"""
            try:
                anio = AnioEscolar.objects.get(pk=pk)
            except AnioEscolar.DoesNotExist:
                return Response({
                    "message": "Año escolar no encontrado."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = AnioEscolarSerializer(anio, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Año escolar actualizado con éxito.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                "message": "Error al actualizar el año escolar.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, pk):
            """Eliminar un año escolar"""
            try:
                anio = AnioEscolar.objects.get(pk=pk)
                anio.delete()
                return Response({
                    "message": "Año escolar eliminado con éxito."
                }, status=status.HTTP_200_OK)
            except AnioEscolar.DoesNotExist:
                return Response({
                    "message": "Año escolar no encontrado."
                }, status=status.HTTP_404_NOT_FOUND)

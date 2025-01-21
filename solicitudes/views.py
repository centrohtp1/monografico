from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Registration
from .serializers import RegistrationSerializer

class RegistrationCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Registro creado exitosamente",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Error al crear el registro",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class RegistrationListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        registrations = Registration.objects.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response({
            "message": "Lista de registros obtenida exitosamente",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class RegistrationDetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            registration = Registration.objects.get(pk=pk)
            serializer = RegistrationSerializer(registration)
            return Response({
                "message": "Registro obtenido exitosamente",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Registration.DoesNotExist:
            return Response({
                "message": "Registro no encontrado"
            }, status=status.HTTP_404_NOT_FOUND)
        

class RegistrationDeleteAPIView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            registration = Registration.objects.get(pk=pk)
            registration.delete()
            return Response({
                "message": "Registro eliminado exitosamente"
            }, status=status.HTTP_204_NO_CONTENT)
        except Registration.DoesNotExist:
            return Response({
                "message": "Registro no encontrado"
            }, status=status.HTTP_404_NOT_FOUND)

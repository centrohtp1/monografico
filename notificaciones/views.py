
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notificacion
from .serializers import NotificacionSerializer
from django.http import JsonResponse

class NotificacionListView(APIView):
    def get(self, request):
        # Obtener todas las notificaciones
        notificaciones = Notificacion.objects.all().order_by('-fecha_creacion')

        # Serializar los objetos de notificación
        serializer = NotificacionSerializer(notificaciones, many=True)

        # Retornar la respuesta en formato JSON
        return Response(serializer.data, status=status.HTTP_200_OK)

# También puedes agregar un endpoint para marcar las notificaciones como leídas.
class MarcarComoLeidaView(APIView):
    def post(self, request, notificacion_id):
        try:
            # Obtener la notificación
            notificacion = Notificacion.objects.get(id=notificacion_id)
            notificacion.leido = True
            notificacion.save()

            return JsonResponse({'message': 'Notificación marcada como leída'}, status=status.HTTP_200_OK)

        except Notificacion.DoesNotExist:
            return JsonResponse({'error': 'Notificación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import serializers
from .models import Notificacion

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'titulo', 'mensaje', 'seccion', 'fecha_creacion', 'leido']
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from datetime import timedelta
from .models import Notificacion
from secciones.models import Seccion
from .serializers import NotificacionSerializer




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from datetime import timedelta
from .models import Notificacion
from secciones.models import Seccion
from .serializers import NotificacionSerializer

class GenerarNotificacionesAPIView(APIView):
    """
    API para generar y guardar notificaciones basadas en secciones próximas a finalizar.
    """
    def get(self, request):
        try:
            hoy = now().date()
            proximos_dias = hoy + timedelta(days=7)
            secciones = Seccion.objects.filter(fecha_termino__range=(hoy, proximos_dias)).select_related('curso')

            notificaciones_generadas = []
            for seccion in secciones:
                # Verificar si ya existe una notificación para esta sección
                if Notificacion.objects.filter(seccion=seccion, leido=False).exists():
                    # Si existe, no crear una nueva
                    continue

                titulo = f"Sección {seccion.nombre} próxima a finalizar"
                mensaje = f"La sección {seccion.nombre} del curso {seccion.curso.nombre} finalizará el {seccion.fecha_termino}."

                # Crear los datos para la notificación
                notificacion_data = {
                    "titulo": titulo,
                    "mensaje": mensaje,
                    "seccion": seccion.id,  # Usamos el ID de la sección para el campo 'seccion'
                }

                # Usar el serializer para validar y crear la notificación
                serializer = NotificacionSerializer(data=notificacion_data)
                if serializer.is_valid():
                    notificacion = serializer.save()  # Guardar la notificación en la base de datos
                    notificaciones_generadas.append(serializer.data)  # Guardamos los datos serializados

            return Response({
                "mensaje": f"{len(notificaciones_generadas)} notificaciones generadas.",
                "notificaciones": notificaciones_generadas
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": f"Ocurrió un error al generar notificaciones: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class NotificacionesNoLeidasView(APIView):
    def get(self, request):
        notificaciones = Notificacion.objects.filter(leido=False)
        serializer = NotificacionSerializer(notificaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MarcarComoLeidaView(APIView):
    def post(self, request, pk):
        try:
            notificacion = Notificacion.objects.get(pk=pk)
            notificacion.leido = True
            notificacion.save()
            return Response({"message": "Notificación marcada como leída."}, status=status.HTTP_200_OK)
        except Notificacion.DoesNotExist:
            return Response({"error": "Notificación no encontrada."}, status=status.HTTP_404_NOT_FOUND)

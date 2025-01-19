from celery import shared_task
from .models import Notificacion
from secciones.models import Seccion
from datetime import timedelta
from django.utils.timezone import now
import logging

# Configurar el logger para la tarea
logger = logging.getLogger(__name__)


@shared_task
def generar_notificaciones_secciones():
    hoy = now().date()
    proximos_dias = hoy + timedelta(days=7)
    notificaciones = []

    # Optimización de la consulta
    secciones = Seccion.objects.filter(fecha_termino__range=(hoy, proximos_dias)).select_related('grado')

    logger.info(f"Secciones encontradas: {secciones.count()}")

    for seccion in secciones:
        titulo = f"Sección {seccion.nombre} próxima a finalizar"
        mensaje = f"La sección {seccion.nombre} del curso {seccion.grado.nombre} finalizará el {seccion.fecha_termino}."

        try:
            notificacion, created = Notificacion.objects.get_or_create(
                titulo=titulo,
                mensaje=mensaje,
                seccion=seccion
            )
            logger.info(f"Notificación {'creada' if created else 'ya existente'}: {notificacion.titulo}")
            notificaciones.append(notificacion)
        except Exception as e:
            logger.error(f"Error al crear notificación para la sección {seccion.nombre}: {e}")

    return f"{len(notificaciones)} notificaciones generadas."
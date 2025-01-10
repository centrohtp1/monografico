from django.http import JsonResponse
from estudiantes.models import Estudiante
import pandas as pd
from django.http import JsonResponse
from facturacion.models import Tarifa
from django.http import JsonResponse
from secciones.models import Seccion
from profesores.models import Profesor
from facturacion.models import Factura
from Cursos.models import Curso


def get_estudiantes_report(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio = pd.to_datetime(fecha_inicio)
            fecha_fin = pd.to_datetime(fecha_fin)
        except ValueError:
            return JsonResponse({'error': 'Formato de fecha incorrecto'}, status=400)

        # Filtrar estudiantes por el rango de fechas de ingreso
        estudiantes = Estudiante.objects.filter(fecha_ingreso__range=(fecha_inicio, fecha_fin))

        # Crear una lista con los datos de los estudiantes
        estudiantes_data = list(estudiantes.values('id', 'matricula','nombre', 'apellido', 'fecha_ingreso'))

        # Retornar el JSON con los datos de los estudiantes
        return JsonResponse({'estudiantes': estudiantes_data}, status=200)
    else:
        return JsonResponse({'error': 'Por favor proporciona las fechas de inicio y fin'}, status=400)
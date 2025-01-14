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


from django.core.exceptions import ValidationError
from anio_escolar import AnioEscolar




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
    




def obtener_anos_escolares(request):

 #   Vista para obtener los años escolares dentro de un rango de fechas ('desde' y 'hasta').
 #   Recibe dos parámetros de consulta: 'desde' (fecha de inicio) y 'hasta' (fecha de fin).
   
    # Obtener los parámetros 'desde' y 'hasta' de la query string
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    # Validación de los parámetros
    if not desde or not hasta:
        return JsonResponse({'error': 'Los parámetros "desde" y "hasta" son obligatorios.'}, status=400)

    try:
        # Convertir los valores de 'desde' y 'hasta' a fechas
        desde = pd.to_datetime(desde)
        hasta = pd.to_datetime(hasta)

    except ValueError:
        return JsonResponse({'error': 'Los parámetros "desde" y "hasta" deben tener el formato de fecha correcto (YYYY-MM-DD).'}, status=400)

    # Filtrar los años escolares dentro del rango de fechas
    anos_escolares = AnioEscolar.objects.filter(
        fecha_ingreso__range=(desde, hasta)
    ).order_by('fecha_ingreso')

    # Verificar si se encontraron años escolares
    if not anos_escolares.exists():
        return JsonResponse({'info': 'No se encontraron años escolares en el rango especificado.'}, status=404)

    # Crear una lista con los datos de los años escolares
    anos_escolares_data = list(anos_escolares.values('id', 'nombre', 'activo', 'fecha_ingreso'))

    # Retornar el JSON con los datos de los años escolares
    return JsonResponse({'anos_escolares': anos_escolares_data}, status=200)



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
from anio_escolar.models import AnioEscolar
from django.utils import timezone




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
    





def get_anos_escolares(request):
    # Obtener los parámetros 'desde' y 'hasta' de la query string
    desde = request.GET.get('fecha_inicio')
    hasta = request.GET.get('fecha_fin')

    # Obtener la fecha actual
    fecha_actual = timezone.now().date()

    # Validación de los parámetros
    if desde and hasta:
        try:
            # Convertir las fechas 'desde' y 'hasta' a objetos de fecha utilizando pandas
            desde = pd.to_datetime(desde)
            hasta = pd.to_datetime(hasta)
        except ValueError:
            return JsonResponse({'error': 'Formato de fecha incorrecto'}, status=400)

        # Filtrar los años escolares dentro del rango de fechas
        anos_escolares = AnioEscolar.objects.filter(fecha_ingreso__range=(desde, hasta))

        # Verificar si hay algún registro con la fecha actual
        anos_escolares_actual = AnioEscolar.objects.filter(fecha_ingreso=fecha_actual)

        # Combinar los resultados (sin duplicados)
        anos_escolares = anos_escolares | anos_escolares_actual

        # Crear una lista con los datos de los años escolares
        anio_data = list(anos_escolares.values('id', 'nombre', 'activo', 'fecha_ingreso'))

        # Retornar el JSON con los datos de los años escolares
        return JsonResponse({'anos_escolares': anio_data}, status=200)
    
    else:
        return JsonResponse({'error': 'Por favor proporciona las fechas "desde" y "hasta"'}, status=400)

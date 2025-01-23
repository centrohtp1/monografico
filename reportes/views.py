
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
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404
from secciones.models import Seccion, SeccionEstudiante
from django.core.exceptions import ValidationError
from anio_escolar.models import AnioEscolar
from django.utils import timezone
from rest_framework import status


@api_view(['GET'])
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
    




@api_view(['GET'])
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
        anios = AnioEscolar.objects.filter(fecha_ingreso__range=(desde, hasta))

        # Verificar si hay algún registro con la fecha actual
        anos_escolares_actual = AnioEscolar.objects.filter(fecha_ingreso=fecha_actual)

        # Combinar los resultados (sin duplicados)
        anios = anios | anos_escolares_actual

        # Crear una lista con los datos de los años escolares
        estudiantes_data = list(anios.values('id', 'nombre', 'activo', 'fecha_ingreso'))

        # Retornar el JSON con los datos de los años escolares
        return JsonResponse({'anios': estudiantes_data}, status=200)
    
    else:
        return JsonResponse({'error': 'Por favor proporciona las fechas "desde" y "hasta"'}, status=400)


@api_view(['GET'])
def get_profesores(request):
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
        profesores = Profesor.objects.filter(fecha_contratacion__range=(desde, hasta))

        # Verificar si hay algún registro con la fecha actual
        anos_escolares_actual = Profesor.objects.filter(fecha_contratacion=fecha_actual)

        # Combinar los resultados (sin duplicados)
        profesores = profesores | anos_escolares_actual

        # Crear una lista con los datos de los años escolares
        estudiantes_data = list(profesores.values('id', 'nombre', 'apellido', 'especialidad','telefono'))

        # Retornar el JSON con los datos de los años escolares
        return JsonResponse({'profesores': estudiantes_data}, status=200)
    
    else:
        return JsonResponse({'error': 'Por favor proporciona las fechas "desde" y "hasta"'}, status=400)
    
@api_view(['GET'])
def get_cursos(request):
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
        cursos = Curso.objects.filter(fecha_creacion__range=(desde, hasta))

        # Verificar si hay algún registro con la fecha actual
        anos_escolares_actual = Curso.objects.filter(fecha_creacion=fecha_actual)

        # Combinar los resultados (sin duplicados)
        cursos = cursos | anos_escolares_actual
        cursos = cursos.select_related('profesores')
        # Crear una lista con los datos de los años escolares
        estudiantes_data = list(cursos.values('id', 'nombre', 'descripcion', 'profesores__nombre'))

        # Retornar el JSON con los datos de los años escolares
        return JsonResponse({'cursos': estudiantes_data}, status=200)
    
    else:
        return JsonResponse({'error': 'Por favor proporciona las fechas "desde" y "hasta"'}, status=400)
    

@api_view(['GET'])
def get_secciones(request):
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
        secciones = Seccion.objects.filter(fecha_inicio__range=(desde, hasta))

        # Verificar si hay algún registro con la fecha actual
        anos_escolares_actual = Seccion.objects.filter(fecha_inicio=fecha_actual)

        # Combinar los resultados (sin duplicados)
        secciones = secciones | anos_escolares_actual
        secciones = secciones.select_related('profesores')
        # Crear una lista con los datos de los años escolares
        estudiantes_data = list(secciones.values('id', 'nombre', 'curso__nombre', 'fecha_inicio', 'fecha_termino','profesores__nombre'))

        # Retornar el JSON con los datos de los años escolares
        return JsonResponse({'secciones': estudiantes_data}, status=200)
    
    else:
        return JsonResponse({'error': 'Por favor proporciona las fechas "desde" y "hasta"'}, status=400)
    

@api_view(['GET'])
def obtener_estudiantes_por_seccion(request, seccion_id):
    try:
        # Obtener la sección por ID, si no existe retornar un error 404
        seccion = get_object_or_404(Seccion, id=seccion_id)

        # Obtener los estudiantes asociados a la sección
        estudiantes_seccion = SeccionEstudiante.objects.filter(seccion=seccion)

        # Verificar si la sección tiene estudiantes
        if not estudiantes_seccion.exists():
            return JsonResponse({'error': 'No hay estudiantes asignados a esta sección'}, status=status.HTTP_404_NOT_FOUND)

        # Preparar los datos de los estudiantes
        estudiantes_data = []

        for seccion_estudiante in estudiantes_seccion:
            estudiante = seccion_estudiante.estudiante
            estudiantes_data.append({
                'id': estudiante.id,
                'nombre': estudiante.nombre,
                'apellido': estudiante.apellido,
                'estado': seccion_estudiante.estado,
                'nota': seccion_estudiante.nota,
            })

        # Retornar la respuesta en formato JSON
        return JsonResponse({'estudiantes': estudiantes_data}, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Si ocurre cualquier otro error, retornar un error genérico
        return JsonResponse({'error': f'Ocurrió un error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



@api_view(['GET'])
def get_tarifas(request):
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
        tar = Tarifa.objects.filter(fecha_creacion__range=(desde, hasta))

        # Verificar si hay algún registro con la fecha actual
        anos_escolares_actual = Tarifa.objects.filter(fecha_creacion=fecha_actual)

        # Combinar los resultados (sin duplicados)
        tar = tar | anos_escolares_actual
        tar = tar.select_related('secciones_tarifa')

        # Crear una lista con los datos de los años escolares
        estudiantes_data = list(tar.values( 'secciones_tarifa__nombre', 'precio', 'fecha_creacion'))

        # Retornar el JSON con los datos de los años escolares
        return JsonResponse({'tarifas': estudiantes_data}, status=200)
    
    else:
        return JsonResponse({'error': 'Por favor proporciona las fechas "desde" y "hasta"'}, status=400)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

import pandas as pd
from django.utils import timezone

@api_view(['GET'])
def get_facturas(request):
    # Obtener los parámetros 'desde' y 'hasta' de la query string
    desde = request.GET.get('fecha_inicio')
    hasta = request.GET.get('fecha_fin')

    # Validación de los parámetros
    if desde and hasta:
        try:
            # Convertir las fechas 'desde' y 'hasta' a objetos de fecha utilizando pandas
            desde = pd.to_datetime(desde)
            hasta = pd.to_datetime(hasta)
        except ValueError:
            return JsonResponse({'error': 'Formato de fecha incorrecto'}, status=400)

        # Filtrar las facturas dentro del rango de fechas
        facturas = Factura.objects.filter(fecha_emision__range=(desde, hasta))

        # Usar select_related para traer la información del estudiante y cuenta por cobrar
        facturas = facturas.select_related('estudiante', 'cuenta_por_cobrar', 'cuenta_por_cobrar__seccion')

        # Crear una lista con los datos de las facturas
        facturas_data = list(facturas.values(
            'numero_factura',
            'estudiante__nombre',  # Accedemos al nombre del estudiante
            'cuenta_por_cobrar__seccion__nombre',  # Accedemos al nombre de la sección de la cuenta por cobrar
            'cuenta_por_cobrar__monto',  # Monto de la cuenta por cobrar
            'cuenta_por_cobrar__estado',  # Estado de la cuenta por cobrar
            'cuenta_por_cobrar__fecha_factura',  # Fecha de la factura asociada
            'cuenta_por_cobrar__mes_correspondiente',  # Mes correspondiente
            'fecha_emision',  # Fecha de emisión de la factura
            'total',  # Total de la factura
            'pagado',  # Si la factura ha sido pagada o no
            'mes_correspondiente'  # Mes correspondiente a la factura
        ))

        # Retornar el JSON con los datos de las facturas
        return JsonResponse({'facturas': facturas_data}, status=200)
    
    else:
        return JsonResponse({'error': 'Por favor proporciona las fechas "desde" y "hasta"'}, status=400)

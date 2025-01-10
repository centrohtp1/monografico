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

from django.db.models import Sum, F


from datetime import datetime

# Función auxiliar para validar fechas
def validar_fechas(fecha_inicio, fecha_fin):
    try:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        return fecha_inicio, fecha_fin
    except ValueError:
        return None, None

# Reporte de Secciones con filtro por fechas
def get_secciones_report(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    fecha_inicio, fecha_fin = validar_fechas(fecha_inicio, fecha_fin)

    if not fecha_inicio or not fecha_fin:
        return JsonResponse({'error': 'Fechas no válidas'}, status=400)

    # Filtrar secciones entre las fechas de inicio y término
    secciones = Seccion.objects.filter(fecha_inicio__range=(fecha_inicio, fecha_fin))
    if not secciones.exists():
        return JsonResponse({'error': 'No se encontraron secciones en el rango de fechas'}, status=404)

    data = [
        {
            'id': s.id,
            'nombre': s.nombre,
            'descripcion': s.descripcion,
            'fecha_inicio': s.fecha_inicio,
            'fecha_termino': s.fecha_termino
        }
        for s in secciones
    ]
    return JsonResponse({'secciones': data}, status=200)

# Reporte de Cursos (filtrado por las secciones asociadas con fechas)
def get_cursos_report(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    fecha_inicio, fecha_fin = validar_fechas(fecha_inicio, fecha_fin)

    if not fecha_inicio or not fecha_fin:
        return JsonResponse({'error': 'Fechas no válidas'}, status=400)

    # Obtener las secciones que caen dentro del rango de fechas
    secciones = Seccion.objects.filter(fecha_inicio__range=(fecha_inicio, fecha_fin))
    if not secciones.exists():
        return JsonResponse({'error': 'No se encontraron secciones en el rango de fechas'}, status=404)

    cursos = Curso.objects.filter(seccion__in=secciones).distinct()
    if not cursos.exists():
        return JsonResponse({'error': 'No se encontraron cursos asociados a las secciones en el rango de fechas'}, status=404)

    data = [
        {
            'id': c.id,
            'nombre_del_curso': c.nombre,
            'descripcion': c.descripcion,
            'profesor': c.profesores.nombre if c.profesores else 'N/A'
        }
        for c in cursos
    ]
    return JsonResponse({'cursos': data}, status=200)

# Reporte de Profesores (filtrado por las secciones en las que enseñan)
def get_profesores_report(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    fecha_inicio, fecha_fin = validar_fechas(fecha_inicio, fecha_fin)

    if not fecha_inicio or not fecha_fin:
        return JsonResponse({'error': 'Fechas no válidas'}, status=400)

    # Obtener las secciones dentro del rango de fechas
    secciones = Seccion.objects.filter(fecha_inicio__range=(fecha_inicio, fecha_fin))
    if not secciones.exists():
        return JsonResponse({'error': 'No se encontraron secciones en el rango de fechas'}, status=404)

    profesores = Profesor.objects.filter(seccion__in=secciones).distinct()
    if not profesores.exists():
        return JsonResponse({'error': 'No se encontraron profesores asociados a las secciones en el rango de fechas'}, status=404)

    data = [
        {
            'id': p.id,
            'nombre': p.nombre,
            'apellido': p.apellido,
            'especialidad': p.especialidad,
            'telefono': p.telefono,
            'fecha_contratacion': p.fecha_contratacion
        }
        for p in profesores
    ]
    return JsonResponse({'profesores': data}, status=200)




# Reporte de Tarifas
def get_tarifas_report(request):
    tarifas = Tarifa.objects.all()
    if not tarifas.exists():
        return JsonResponse({'error': 'No se encontraron tarifas'}, status=404)

    data = [
        {
            'id': t.id,
            'concepto': f"Tarifa para {t.secciones_tarifa.nombre}",
            'costo': t.precio
        }
        for t in tarifas
    ]
    return JsonResponse({'tarifas': data}, status=200)

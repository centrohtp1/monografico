# estudiantes/views.py

from django.http import JsonResponse
from .models import Estudiante
import pandas as pd
import io
from django.template.loader import render_to_string
from xhtml2pdf import pisa

def get_estudiantes_report(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio = pd.to_datetime(fecha_inicio)
            fecha_fin = pd.to_datetime(fecha_fin)
        except ValueError:
            return JsonResponse({'error': 'Formato de fecha incorrecto'}, status=400)
        
        # Filtrar estudiantes por el rango de fechas de nacimiento
        estudiantes = Estudiante.objects.filter(fecha_ingreso__range=(fecha_inicio, fecha_fin))
        
        # Generar DataFrame
        df = pd.DataFrame(list(estudiantes.values()))
        
        # Generar PDF
        template = render_to_string('estudiantes/report_pdf.html', {'estudiantes': df})
        pdf_io = io.BytesIO()
        pisa_status = pisa.CreatePDF(template, dest=pdf_io)
        
        # Generar Excel
        excel_io = io.BytesIO()
        df.to_excel(excel_io, index=False, engine='openpyxl')
        
        # Enviar el archivo PDF y Excel como respuesta
        return JsonResponse({
            'pdf_data': pdf_io.getvalue().decode('latin1'),
            'excel_data': excel_io.getvalue().decode('latin1')
        }, safe=False)
    else:
        return JsonResponse({'error': 'Por favor proporciona las fechas de inicio y fin'}, status=400)
from django.shortcuts import render

# Create your views here.

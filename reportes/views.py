from django.http import JsonResponse, HttpResponse
from estudiantes.models import Estudiante
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
        
        # Filtrar estudiantes por el rango de fechas
        estudiantes = Estudiante.objects.filter(fecha_ingreso__range=(fecha_inicio, fecha_fin))
        
        # Preparar contexto para el template
        df = pd.DataFrame(list(estudiantes.values()))
        template = render_to_string('estudiantes/report_pdf.html', {'estudiantes': df})
        
        # Generar PDF
        pdf_io = io.BytesIO()
        pisa_status = pisa.CreatePDF(template, dest=pdf_io)
        
        if pisa_status.err:
            return JsonResponse({'error': 'Error al generar el PDF'}, status=500)
        
        # Preparar respuesta HTTP con el PDF
        pdf_io.seek(0)
        response = HttpResponse(pdf_io, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="reporte_estudiantes.pdf"'
        return response
    else:
        return JsonResponse({'error': 'Por favor proporciona las fechas de inicio y fin'}, status=400)

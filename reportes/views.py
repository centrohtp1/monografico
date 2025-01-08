from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
from estudiantes.models import Estudiante
import pandas as pd

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
        
        # Generar contenido HTML para el PDF
        template = render_to_string('estudiantes/report_pdf.html', {'estudiantes': estudiantes})
        
        # Generar el PDF
        pdf_io = io.BytesIO()
        pisa_status = pisa.CreatePDF(template, dest=pdf_io)
        
        if pisa_status.err:
            return JsonResponse({'error': 'Error al generar el PDF'}, status=500)
        
        # Configurar la respuesta para descargar el PDF
        response = HttpResponse(pdf_io.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_estudiantes.pdf"'
        return response
    else:
        return JsonResponse({'error': 'Por favor proporciona las fechas de inicio y fin'}, status=400)

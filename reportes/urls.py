# estudiantes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('reporte-estudiantes/', views.get_estudiantes_report, name='get_estudiantes_report'),
      # Reporte de Secciones
    path('reporte-secciones/', views.get_secciones_report, name='reporte_secciones'),

    # Reporte de Cursos
    path('reporte-cursos/', views.get_cursos_report, name='reporte_cursos'),

    # Reporte de Profesores
    path('reporte-profesores/', views.get_profesores_report, name='reporte_profesores'),

    # Reporte de Facturas
    path('reporte-facturas/', views.get_facturas_report, name='reporte_facturas'),

    # Reporte de Tarifas
    path('reporte-tarifas/', views.get_tarifas_report, name='reporte_tarifas'),
]



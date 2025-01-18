# estudiantes/urls.py
from django.urls import path
from reportes import views

urlpatterns = [
    path('reporte-estudiantes/', views.get_estudiantes_report, name='get_estudiantes_report'),
    path('reportes-anioescolar/', views.get_anos_escolares, name='get_anos_escolares'),
       path('reportes-profesores/', views.get_profesores, name='get_profesores'),
          path('reportes-cursos/', views.get_cursos, name='get_cursos'),
          path('reportes-secciones/', views.get_secciones, name='get_secciones'),
            path('reportes-estudiantes-secciones/<int:seccion_id>/', views.obtener_estudiantes_por_seccion, name='obtener_estudiantes_por_seccion'),

]



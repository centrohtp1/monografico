# estudiantes/urls.py
from django.urls import path
from reportes import views

urlpatterns = [
    path('reporte-estudiantes/', views.get_estudiantes_report, name='get_estudiantes_report'),
    path('reportes-anioescolar/', views.get_anos_escolares, name='get_anos_escolares'),

]



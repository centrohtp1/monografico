# estudiantes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('reporte-estudiantes/', views.get_estudiantes_report, name='get_estudiantes_report'),
]


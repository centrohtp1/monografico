from django.urls import path
from . import views

urlpatterns = [
    path('contactos/', views.listar_contactos, name='listar_contactos'),
    path('contactos/crear/', views.crear_contacto, name='crear_contacto'),
    path('contactos/eliminar/<int:pk>/', views.eliminar_contacto, name='eliminar_contacto'),
]

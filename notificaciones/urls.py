# notificaciones/urls.py
from django.urls import path
from .views import GenerarNotificacionesAPIView, NotificacionesNoLeidasView, MarcarComoLeidaView

urlpatterns = [
    path('no-leidas/', NotificacionesNoLeidasView.as_view(), name='notificaciones-no-leidas'),
    path('marcar-como-leida/<int:pk>/', MarcarComoLeidaView.as_view(), name='marcar-como-leida'),
       path('generar-notificaciones/', GenerarNotificacionesAPIView.as_view(), name='generar-notificaciones'),
    
]

# notificaciones/urls.py
from django.urls import path
from .views import NotificacionListView, MarcarComoLeidaView

urlpatterns = [
    path('api/notificaciones/', NotificacionListView.as_view(), name='api_listar_notificaciones'),
    path('api/notificaciones/marcar_leida/<int:notificacion_id>/', MarcarComoLeidaView.as_view(), name='api_marcar_como_leida'),
]
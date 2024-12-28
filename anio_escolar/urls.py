# anio_escolar/urls.py
from django.urls import path
from .views import AnioEscolarCRUDView

urlpatterns = [
    path('', AnioEscolarCRUDView.as_view(), name='anios-escolares'),
    path('anios-escolares/<int:pk>/', AnioEscolarCRUDView.as_view(), name='anio-escolar-detail'),
]

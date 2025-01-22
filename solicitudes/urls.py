from django.urls import path
from .views import RegistrationCreateAPIView, RegistrationDeleteAPIView, RegistrationListAPIView, RegistrationDetailAPIView

urlpatterns = [
    path('api/registrations/', RegistrationCreateAPIView.as_view(), name='registration-create'),
    path('api/registrations/list/', RegistrationListAPIView.as_view(), name='registration-list'),
    path('api/registrations/<int:pk>/', RegistrationDetailAPIView.as_view(), name='registration-detail'),
    path('registrations/<int:pk>/', RegistrationDeleteAPIView.as_view(), name='registration-delete'),
 
]

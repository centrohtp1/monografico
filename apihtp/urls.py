"""
URL configuration for apihtp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API de Secciones",
      default_version='v1',
      description="Documentación de la API para gestionar secciones y estudiantes",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@tuapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [


         path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
  
    path('admin/', admin.site.urls),
     path('profesores/', include('profesores.urls')),  # API para "profesores"
      path('solicitudes/', include('solicitudes.urls')),  # API para "profesores"
    path('estudiantes/', include('estudiantes.urls')),  # API para "estudiantes"
      path('cursos/', include('Cursos.urls')),  # API para "estudiantes"
             path('contactanos/', include('contactanos.urls')),  # API para "secciones"
         path('usuarios/', include('usuarioshtp.urls')),  
         path('anioescolar/', include('anio_escolar.urls')),  # API para "secciones"
         path('reporte/', include('reportes.urls')),  # Incluir las URLs de la app "facturacion"
              path('notificaciones/', include('notificaciones.urls')),  # Incluir las URLs de la app "facturacion"
     
      path('secciones/', include('secciones.urls')),  # Incluir las URLs de la app "secciones"
    path('facturacion/', include('facturacion.urls')),  # Incluir las URLs de la app "facturacion"
  
]

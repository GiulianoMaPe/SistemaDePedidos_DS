from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('inicio.urls')),

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), #Ruta del API

    path('pedidos/', include('pedidos.urls')),

    path('productos/', include('productos.urls')),


]

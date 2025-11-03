from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Ruta del API
    path('api/', include('api.urls')),

    # Esto conecta la URL 'pedidos/' con el nuevo archivo 'pedidos/urls.py'
    path('pedidos/', include('pedidos.urls')),
]

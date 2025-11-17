from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('inicio.urls')),

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), #Ruta del API

    path('pedidos/', include('pedidos.urls')),

    path('productos/', include('productos.urls')),

    path('usuarios/', include('usuarios.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
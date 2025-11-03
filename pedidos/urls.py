# En: pedidos/urls.py
from django.urls import path
from . import views  # Importa las vistas de esta misma carpeta (app)

urlpatterns = [
    # Cuando el usuario visite la raíz de 'pedidos/' (ej: .../pedidos/),
    # se ejecutará la función 'vista_inicio' que crearemos en el siguiente paso.
    path('', views.vista_inicio, name='inicio-pedidos'),
]
from django.urls import path
from . import views

urlpatterns = [
    #HU-05
    path('admin/', views.administrar_productos_vista, name='admin-productos'),

    path('agregar/', views.agregar_producto_vista, name='agregar-producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto_vista, name='eliminar-producto'),
]
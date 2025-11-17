from django.urls import path
from . import views

urlpatterns = [
    #HU-05
    path('admin/', views.administrar_productos_vista, name='admin-productos'),

    # Productos
    path('agregar/', views.agregar_producto_vista, name='agregar-producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto_vista, name='eliminar-producto'),

    # Insumos
    path('insumo/agregar/', views.agregar_insumo_vista, name='agregar-insumo'),
    path('insumo/editar/', views.editar_insumo_vista, name='editar-insumo'),  # NUEVA RUTA
    path('insumo/eliminar/<int:insumo_id>/', views.eliminar_insumo_vista, name='eliminar-insumo'),
]
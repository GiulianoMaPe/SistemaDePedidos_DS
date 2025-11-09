from django.urls import path
from . import views

urlpatterns = [
    #HU-04
    path('menu/', views.menu_digital_vista, name='menu-digital'),
    #HU-05
    path('admin/', views.administrar_productos_vista, name='admin-productos'),
]
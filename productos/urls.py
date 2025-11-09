from django.urls import path
from . import views

urlpatterns = [
    #HU-05
    path('admin/', views.administrar_productos_vista, name='admin-productos'),
]
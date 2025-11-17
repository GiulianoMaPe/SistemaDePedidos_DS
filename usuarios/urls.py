from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_cajero_vista, name='login-cajero'),
    path('login/admin/', views.login_admin_vista, name='login-admin'),

    # --- URLs para la HU Administrar Cuentas ---

    # (R)ead: Página principal que lista al personal
    path('admin/personal/', views.admin_personal_vista, name='admin-personal'),

    # (C)reate: Ruta que procesa el formulario para agregar un nuevo cajero
    path('admin/personal/agregar/', views.agregar_cajero_vista, name='agregar-cajero'),

    # (U)pdate: Ruta que procesa el formulario para modificar un cajero existente
    path('admin/personal/modificar/<int:user_id>/', views.modificar_cajero_vista, name='modificar-cajero'),

    # (D)elete: Ruta que elimina un cajero
    path('admin/personal/eliminar/<int:user_id>/', views.eliminar_cajero_vista, name='eliminar-cajero'),
]
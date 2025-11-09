from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_cajero_vista, name='login-cajero'),
    path('login/admin/', views.login_admin_vista, name='login-admin'),
]
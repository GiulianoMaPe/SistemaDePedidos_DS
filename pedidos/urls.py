from django.urls import path
from . import views

urlpatterns = [
    #HU-01
    path('registrar/', views.registrar_pedido_vista, name='registrar-pedido'),
    #HU-02
    path('personalizar/<int:producto_id>/', views.personalizar_producto_vista, name='personalizar-producto'),
    #HU-03
    path('panel/', views.panel_pedidos_vista, name='panel-pedidos'),
    path('actualizar-estado/<int:pedido_id>/', views.actualizar_estado_vista, name='actualizar-estado'),
]
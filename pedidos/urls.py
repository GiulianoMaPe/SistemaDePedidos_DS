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
    #HU-04: Historial de ventas
    path('historial/', views.historial_ventas_vista, name='historial-ventas'),
    # HU-09: Registro de ventas
    path('exportar-ventas-pdf/', views.exportar_ventas_pdf, name='exportar-ventas-pdf'),
    path('exportar-ventas-excel/', views.exportar_ventas_excel, name='exportar-ventas-excel'),
    path('historial/detalle/<int:pedido_id>/', views.detalle_venta_vista, name='detalle-venta'),
    # Panel de administrador
    path('panel-admin/', views.panel_pedidos_admin_vista, name='panel-pedidos-admin'),
    path('finalizar-dia/', views.finalizar_dia_vista, name='finalizar-dia'),
]
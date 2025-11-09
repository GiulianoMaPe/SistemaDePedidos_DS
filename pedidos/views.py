from django.shortcuts import render, redirect, get_object_or_404
from productos.models import Producto
from .models import Pedido

#HU-01: Registrar nuevo pedido
def registrar_pedido_vista(request):
    productos = Producto.objects.all()
    contexto = {
        'productos': productos
    }
    return render(request, 'pedidos/registrar_pedido.html', contexto)

#HU-02: Personalizar producto
def personalizar_producto_vista(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    contexto = {
        'producto': producto
    }
    return render(request, 'pedidos/personalizar_producto.html', contexto)

#HU-03: Actualizar estado de un pedido
def panel_pedidos_vista(request):
    pedidos_activos = Pedido.objects.filter(estado='En preparación')

    contexto = {
        'pedidos': pedidos_activos
    }

    return render(request, 'pedidos/panel_pedidos.html', contexto)

def actualizar_estado_vista(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    #Actualizamos el estado
    pedido.estado = 'Entregado'
    pedido.save()

    return redirect('panel-pedidos')
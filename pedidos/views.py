from django.shortcuts import render, redirect, get_object_or_404
from productos.models import Producto
from django.contrib import messages
from .models import Pedido, DetallePedido
import json


# HU-01: Registrar nuevo pedido
def registrar_pedido_vista(request):
    if request.method == 'POST':
        pedido_data = request.POST.get('pedido_data')

        if pedido_data:
            try:
                # Parsear el JSON del pedido
                pedido_json = json.loads(pedido_data)
                cliente = request.POST.get('cliente', 'Cliente Mostrador')

                # 1. Calcular el total
                total = 0
                for item_id, item in pedido_json.items():
                    precio_base = float(item['precioBase'])
                    cantidad = int(item['cantidad'])
                    # Sumar precio de extras
                    precio_extras = sum(float(extra['precio']) for extra in item.get('extras', []))
                    subtotal = (precio_base + precio_extras) * cantidad
                    total += subtotal

                # 2. Crear el Pedido Padre
                pedido = Pedido.objects.create(
                    cliente=cliente,
                    total=total,
                    estado='En preparación'
                )

                # 3. Crear los detalles
                for item_id, item in pedido_json.items():
                    producto_id = item['pId']
                    cantidad = item['cantidad']

                    # PROCESAR EXTRAS: Convertir lista de objetos a string "Queso, Tocino"
                    lista_extras = [extra['nombre'] for extra in item.get('extras', [])]
                    texto_personalizacion = ", ".join(lista_extras)

                    try:
                        producto = Producto.objects.get(id=producto_id)
                        DetallePedido.objects.create(
                            pedido=pedido,
                            producto=producto,
                            cantidad=cantidad,
                            personalizacion=texto_personalizacion  # ¡Aquí guardamos los datos!
                        )
                    except Producto.DoesNotExist:
                        pass

                messages.success(request, f'Pedido #{pedido.id} registrado exitosamente!')
                return redirect('panel-pedidos')

            except Exception as e:
                messages.error(request, f'Error al procesar: {str(e)}')
        else:
            messages.warning(request, 'El carrito está vacío')

    productos = Producto.objects.all()
    return render(request, 'pedidos/registrar_pedido.html', {'productos': productos})


# HU-02: Personalizar producto
def personalizar_producto_vista(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    contexto = {
        'producto': producto
    }
    return render(request, 'pedidos/personalizar_producto.html', contexto)


# HU-03: Actualizar estado de un pedido
def panel_pedidos_vista(request):
    # Mostrar todos los pedidos excepto los entregados y cancelados
    pedidos_activos = Pedido.objects.exclude(estado__in=['Entregado', 'Cancelado']).order_by('-fecha')

    contexto = {
        'pedidos': pedidos_activos
    }

    return render(request, 'pedidos/panel_pedidos.html', contexto)


def actualizar_estado_vista(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')

        # Validar que el estado sea válido
        estados_validos = ['En preparación', 'Listo para entregar', 'Entregado', 'Cancelado']
        if nuevo_estado in estados_validos:
            pedido.estado = nuevo_estado
            pedido.save()

    return redirect('panel-pedidos')
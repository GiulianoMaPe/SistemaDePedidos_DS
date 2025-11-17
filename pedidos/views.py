from django.shortcuts import render, redirect, get_object_or_404
from productos.models import Producto, Insumo
from django.contrib import messages
from .models import Pedido, DetallePedido
import json

# HU-01: Registrar nuevo pedido
def registrar_pedido_vista(request):
    if request.method == 'POST':
        pedido_data = request.POST.get('pedido_data')

        if pedido_data:
            try:
                pedido_json = json.loads(pedido_data)
                cliente = request.POST.get('cliente', 'Cliente General')

                # 1. Calcular total
                total = 0
                for item_id, item in pedido_json.items():
                    precio_base = float(item['precioBase'])
                    cantidad = int(item['cantidad'])
                    precio_extras = sum(float(extra['precio']) for extra in item.get('extras', []))
                    subtotal = (precio_base + precio_extras) * cantidad
                    total += subtotal

                # 2. Crear Pedido
                pedido = Pedido.objects.create(
                    cliente=cliente,
                    total=total,
                    estado='En preparación'
                )

                # 3. Crear Detalles
                for item_id, item in pedido_json.items():
                    producto_id = item['pId']
                    cantidad = item['cantidad']

                    # Convertir extras a texto para guardar en BD
                    lista_extras = [f"{extra['nombre']} (S/{extra['precio']})" for extra in item.get('extras', [])]
                    texto_personalizacion = ", ".join(lista_extras)

                    try:
                        producto = Producto.objects.get(id=producto_id)
                        DetallePedido.objects.create(
                            pedido=pedido,
                            producto=producto,
                            cantidad=cantidad,
                            personalizacion=texto_personalizacion
                        )
                    except Producto.DoesNotExist:
                        pass

                messages.success(request, f'Pedido #{pedido.id} registrado exitosamente!')
                return redirect('panel-pedidos')

            except Exception as e:
                messages.error(request, f'Error al procesar: {str(e)}')
        else:
            messages.warning(request, 'El carrito está vacío')

    # GET
    # 1. Traemos productos con sus insumos base precargados
    productos_bd = Producto.objects.prefetch_related('insumos').all()

    # 2. Traemos insumos para usarlos como EXTRAS
    insumos_bd = Insumo.objects.all()

    # Convertimos los insumos a una lista de diccionarios para JS
    extras_list = []
    for insumo in insumos_bd:
        extras_list.append({
            'id': insumo.id,
            'nombre': insumo.nombre,
            'precio': float(insumo.precio)  # Convertir Decimal a float para JSON
        })

    # Serializamos a JSON para pasarlo al template
    extras_json = json.dumps(extras_list)

    contexto = {
        'productos': productos_bd,
        'extras_json': extras_json
    }
    return render(request, 'pedidos/registrar_pedido.html', contexto)


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
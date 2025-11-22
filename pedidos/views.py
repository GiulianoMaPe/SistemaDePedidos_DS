from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from productos.models import Producto, Insumo
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

    productos_bd = Producto.objects.prefetch_related('insumos').all()
    insumos_bd = Insumo.objects.all()

    extras_list = []
    for insumo in insumos_bd:
        extras_list.append({
            'id': insumo.id,
            'nombre': insumo.nombre,
            'precio': float(insumo.precio)
        })

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
    pedidos_activos = Pedido.objects.exclude(estado__in=['Entregado', 'Cancelado']).order_by('-fecha')
    contexto = {
        'pedidos': pedidos_activos
    }
    return render(request, 'pedidos/panel_pedidos.html', contexto)


def actualizar_estado_vista(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        estados_validos = ['En preparación', 'Listo para entregar', 'Entregado', 'Cancelado']
        if nuevo_estado in estados_validos:
            pedido.estado = nuevo_estado
            pedido.save()

    return redirect('panel-pedidos')


# HU-04: Consultar historial de ventas
def historial_ventas_vista(request):
    from datetime import datetime, timedelta

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    ventas = Pedido.objects.filter(estado='Entregado').order_by('-fecha')

    if fecha_inicio:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            ventas = ventas.filter(fecha__gte=fecha_inicio_dt)
        except ValueError:
            pass

    if fecha_fin:
        try:
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            fecha_fin_dt = fecha_fin_dt + timedelta(days=1)
            ventas = ventas.filter(fecha__lt=fecha_fin_dt)
        except ValueError:
            pass

    total_ventas = sum(venta.total for venta in ventas)
    cantidad_ventas = ventas.count()

    contexto = {
        'ventas': ventas,
        'total_ventas': total_ventas,
        'cantidad_ventas': cantidad_ventas,
        'fecha_inicio': fecha_inicio or '',
        'fecha_fin': fecha_fin or '',
    }

    return render(request, 'pedidos/historial_ventas.html', contexto)


def detalle_venta_vista(request, pedido_id):
    venta = get_object_or_404(Pedido, id=pedido_id)
    detalles = venta.detalles.all()

    contexto = {
        'venta': venta,
        'detalles': detalles,
    }

    return render(request, 'pedidos/detalle_venta.html', contexto)
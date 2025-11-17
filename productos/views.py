from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto, Insumo

#HU-05: Administrar productos
def administrar_productos_vista(request):
    productos = Producto.objects.all().order_by('-id')
    insumos = Insumo.objects.all().order_by('nombre')

    contexto = {
        'productos': productos,
        'insumos': insumos
    }
    return render(request, 'productos/admin_productos.html', contexto)


def agregar_producto_vista(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            precio_input = request.POST.get('precio')  # Obtener como string
            categoria = request.POST.get('categoria')
            descripcion = request.POST.get('descripcion')

            try:
                precio = float(precio_input)
                if precio < 0:
                    precio = 0.0
            except ValueError:
                precio = 0.0

            nuevo_producto = Producto.objects.create(
                nombre=nombre,
                precio=precio,
                categoria=categoria,
                descripcion=descripcion
            )
            # Asociar insumos seleccionados
            insumos_ids = request.POST.getlist('insumos_ids')
            if insumos_ids:
                insumos_ids = [int(id) for id in insumos_ids]
                nuevo_producto.insumos.set(insumos_ids)

            messages.success(request, f'Producto "{nombre}" agregado correctamente.')

        except Exception as e:
            messages.error(request, f'Error al agregar producto: {str(e)}')

    return redirect('admin-productos')

def eliminar_producto_vista(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    messages.warning(request, 'Producto eliminado.')
    return redirect('admin-productos')


def agregar_insumo_vista(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre').strip()
        stock = request.POST.get('stock', 0)

        # Verificar duplicados
        if Insumo.objects.filter(nombre__iexact=nombre).exists():
            messages.error(request, f'¡El insumo "{nombre}" ya existe!')
            return redirect('admin-productos')

        try:
            Insumo.objects.create(nombre=nombre, stock=stock)
            messages.success(request, 'Insumo agregado.')
        except Exception as e:
            messages.error(request, 'Error al guardar insumo.')

    return redirect('admin-productos')


def editar_insumo_vista(request):
    if request.method == 'POST':
        insumo_id = request.POST.get('insumo_id')
        nuevo_nombre = request.POST.get('nombre')
        nuevo_stock = request.POST.get('stock')

        insumo = get_object_or_404(Insumo, id=insumo_id)

        # Validar nombre duplicado solo si cambió el nombre
        if insumo.nombre.lower() != nuevo_nombre.lower():
            if Insumo.objects.filter(nombre__iexact=nuevo_nombre).exists():
                messages.error(request, 'Ya existe otro insumo con ese nombre.')
                return redirect('admin-productos')

        insumo.nombre = nuevo_nombre
        insumo.stock = nuevo_stock
        insumo.save()
        messages.success(request, 'Insumo actualizado correctamente.')

    return redirect('admin-productos')

def eliminar_insumo_vista(request, insumo_id):
    insumo = get_object_or_404(Insumo, id=insumo_id)
    insumo.delete()
    messages.warning(request, 'Insumo eliminado.')
    return redirect('admin-productos')
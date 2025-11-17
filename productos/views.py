from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto

#HU-05: Administrar productos
def administrar_productos_vista(request):
    productos = Producto.objects.all().order_by('-id')
    contexto = {
        'productos': productos
    }
    return render(request, 'productos/admin_productos.html', contexto)

def agregar_producto_vista(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')

        # Creamos el producto en la BD
        Producto.objects.create(
            nombre=nombre,
            precio=precio,
            categoria=categoria,
            descripcion=descripcion
        )
        return redirect('admin-productos')

    return redirect('admin-productos')

def eliminar_producto_vista(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('admin-productos')
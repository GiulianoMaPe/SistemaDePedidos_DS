from django.shortcuts import render
from .models import Producto

#HU-04: Visualizar menú digital
def menu_digital_vista(request):
    categorias = Producto.objects.values('categoria').distinct()
    productos = Producto.objects.all()
    contexto = {
        'categorias': categorias,
        'productos': productos
    }
    return render(request, 'productos/menu_digital.html', contexto)

#HU-05: Administrar productos
def administrar_productos_vista(request):
    productos = Producto.objects.all()
    contexto = {
        'productos': productos
    }
    return render(request, 'productos/admin_productos.html', contexto)

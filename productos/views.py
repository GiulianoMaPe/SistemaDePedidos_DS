from django.shortcuts import render
from .models import Producto

#HU-05: Administrar productos
def administrar_productos_vista(request):
    productos = Producto.objects.all()
    contexto = {
        'productos': productos
    }
    return render(request, 'productos/admin_productos.html', contexto)

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Esta es la función (Controlador) que faltaba
def vista_inicio(request):
    # Esto le dice a Django que busque y muestre el HTML
    return render(request, 'pedidos/inicio.html')

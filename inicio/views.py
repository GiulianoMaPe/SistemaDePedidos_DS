from django.shortcuts import render

def menu_principal(request):
    return render(request, 'inicio/inicio.html')

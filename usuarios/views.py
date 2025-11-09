from django.shortcuts import render, redirect

def login_cajero_vista(request):
    #POST
    if request.method == 'POST':
        # ---
        # HU-06: Iniciar sesión en el sistema
        # ---
        return redirect('registrar-pedido')

    #GET
    return render(request, 'usuarios/login_cajero.html')

def login_admin_vista(request):
    #POST
    if request.method == 'POST':
        # ---
        # HU-06: Iniciar sesión en el sistema
        # ---
        return redirect('admin-productos')

    #GET
    return render(request, 'usuarios/login_admin.html')

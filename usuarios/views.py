from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

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


# --- Vistas para la HU Administrar Cuentas ---

def admin_personal_vista(request):
    """
    (R)ead: Muestra la lista de todo el personal que NO es superusuario (Administrador).
    Cumple la precondición de estar en la pantalla "Personal".
    """
    # Filtramos para mostrar solo usuarios que no son administradores
    # Asumimos que los cajeros son "is_superuser=False"
    cajeros = User.objects.filter(is_superuser=False).order_by('username')
    contexto = {
        'cajeros': cajeros
    }
    return render(request, 'usuarios/admin_personal.html', contexto)


def agregar_cajero_vista(request):
    """
    (C)reate: Procesa el formulario para crear un nuevo cajero.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        pass_raw = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Criterio de Aceptación 4: Validar usuario único
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Error: El nombre de usuario '{username}' ya existe.")
            return redirect('admin-personal')

        try:
            # Criterio de Aceptación 1: Crear nuevo cajero
            user = User.objects.create_user(
                username=username,
                password=pass_raw,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_staff=True  # Le damos acceso al admin, pero no es superusuario
            )
            messages.success(request, f"Cajero '{username}' creado exitosamente.")

        except IntegrityError:
            messages.error(request, f"Error: El nombre de usuario '{username}' ya existe.")
        except Exception as e:
            messages.error(request, f"Error inesperado: {str(e)}")

    return redirect('admin-personal')


def modificar_cajero_vista(request, user_id):
    """
    (U)pdate: Procesa el formulario para modificar un cajero existente.
    """
    if request.method == 'POST':
        # Criterio de Aceptación 2: Seleccionar y modificar
        user = get_object_or_404(User, id=user_id)

        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        pass_raw = request.POST.get('password')  # Opcional

        # Criterio de Aceptación 4: Validar usuario único (excluyendo al usuario actual)
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, f"Error: El nombre de usuario '{username}' ya pertenece a otra cuenta.")
            return redirect('admin-personal')

        try:
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            # Solo actualizar la contraseña si se proporcionó una nueva
            if pass_raw:
                user.set_password(pass_raw)

            user.save()
            messages.success(request, f"Cajero '{username}' actualizado exitosamente.")

        except Exception as e:
            messages.error(request, f"Error al actualizar: {str(e)}")

    return redirect('admin-personal')


def eliminar_cajero_vista(request, user_id):
    """
    (D)elete: Elimina un cajero de la base de datos.
    """
    # Criterio de Aceptación 3: Seleccionar y eliminar
    user = get_object_or_404(User, id=user_id)

    try:
        username_copia = user.username
        user.delete()
        messages.success(request, f"Cajero '{username_copia}' eliminado permanentemente.")

    except Exception as e:
        messages.error(request, f"Error al eliminar: {str(e)}")

    return redirect('admin-personal')
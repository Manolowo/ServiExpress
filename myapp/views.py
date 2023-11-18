from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import UserProfile

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
                return HttpResponse('Rol no reconocido')
        else:
            # Manejar el caso de usuario o contraseña incorrectos
            return HttpResponse('Usuario o contraseña incorrectos')

    return render(request, 'login.html')
    
def cli_home(request):
    return render(request, 'cli_home.html')

def emp_home(request):
    return render(request, 'emp_home.html')

def adm_home(request):
    return render(request, 'admin/adm_home.html')
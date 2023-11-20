from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from .models import UserProfile
from .models import Servicio
from .models import Proveedor
from .models import Vehiculo
from .models import Atencion


from myapp.carrito import Carrito

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
                return render(request, 'index.html')
        else:
            # Manejar el caso de usuario o contraseña incorrectos
            return render(request, 'index.html')

    return render(request, 'index.html')

def crear_cuenta(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_lastname = request.POST.get('user_lastname')
        user_password = request.POST.get('user_password')
        user_mail = request.POST.get('user_mail')
        user_fono = request.POST.get('user_fono')

        # Crear el objeto UserProfile y asignar el rol
        user_profile = UserProfile(
            user_name=user_name,
            user_lastname=user_lastname,
            user_password=user_password,
            user_mail=user_mail,
            user_fono=user_fono,
            rol_id='cli'  # Asignar el rol 'cli' por defecto
        )
        user_profile.save()

        # Aquí puedes agregar lógica adicional, como iniciar sesión automáticamente

        return redirect('cli_home')  # Cambia 'index' por la URL a la que quieras redirigir después de crear la cuenta

    return render(request, 'crear_cuenta.html')
    
def cli_home(request):
    return render(request, 'cliente/cli_home.html')


def cli_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'cliente/cli_servicios.html', {'servicios': servicios})

@login_required
def cli_vehiculo(request):
    try:
        user_profile = UserProfile.objects.get(user_id=request.session['user_id'])
        print("User ID from session:", request.session.get('user_id'))
        print("User Profile for current user:", user_profile)
    except UserProfile.DoesNotExist:
        # Manejar el caso en que el UserProfile no exista
        return redirect('cli_home')

    # Filtrar los vehículos por el UserProfile del usuario actual
    vehiculo = Vehiculo.objects.filter(userProfile=user_profile)

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            veh_patente = request.POST.get('veh_patente')
            veh_marca = request.POST.get('veh_marca')
            veh_modelo = request.POST.get('veh_modelo')
            veh_anno = request.POST.get('veh_anno')
            veh_img = request.FILES.get('veh_img')

            # Crear y guardar el nuevo vehículo
            nuevo_vehiculo = Vehiculo(
                veh_patente=veh_patente,
                veh_marca=veh_marca,
                veh_modelo=veh_modelo,
                veh_anno=veh_anno,
                veh_img=veh_img,
                userProfile=user_profile
            )
            nuevo_vehiculo.save()

            vehiculo_data = {
                'veh_patente': nuevo_vehiculo.veh_patente,
                'veh_marca': nuevo_vehiculo.veh_marca,
                'veh_modelo': nuevo_vehiculo.veh_modelo,
                'veh_anno': nuevo_vehiculo.veh_anno,
                'veh_img': nuevo_vehiculo.veh_img.url if nuevo_vehiculo.veh_img else None,
                'user_id': nuevo_vehiculo.userProfile.user_id,
            }
            return JsonResponse(vehiculo_data)

        except Exception as e:
            return JsonResponse({'error': str(e)})

    return render(request, 'cliente/cli_vehiculo.html', {'vehiculo': vehiculo})

@login_required
def cli_atencion(request):
    try:
        user_profile = UserProfile.objects.get(user_id=request.session['user_id'])
        print("User ID from session:", request.session.get('user_id'))
        print("User Profile for current user:", user_profile)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'UserProfile no encontrado'})

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            ate_list = request.POST.get('ate_list')
            ate_date = request.POST.get('ate_date')
            ate_prec = request.POST.get('ate_prec')

            # Crear y guardar el nuevo usuario
            addatencion = Atencion(
                ate_list=ate_list,
                ate_date=ate_date,
                ate_prec=ate_prec,
                userProfile=user_profile
            )
            addatencion.save()

            ate_data = {
                'ate_list': addatencion.ate_list,
                'ate_date': addatencion.ate_date.strftime('%Y-%m-%d'),  # Formatear la fecha
                'ate_prec': addatencion.ate_prec,
                'user_id': addatencion.userProfile.user_id,
            }
            return JsonResponse(ate_data)

        except Exception as e:
            return JsonResponse({'error': str(e)})

    atencion = Atencion.objects.filter(userProfile=user_profile)
    return render(request, 'cliente/cli_atencion.html', {'atencion': atencion})


def emp_home(request):
    return render(request, 'personal/per_home.html')

def adm_home(request):
    return render(request, 'admin/adm_home.html')

def adm_users(request):
    users = UserProfile.objects.all()
    return render(request, 'admin/adm_users.html', {'users': users})

def adm_atenciones(request):
    users = UserProfile.objects.all()
    atenciones = Atencion.objects.all()
    vehiculo = Vehiculo.objects.all()
    return render(request, 'admin/adm_atenciones.html', {'vehiculo': vehiculo, 'users': users , 'atenciones': atenciones})

def adm_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'admin/adm_servicios.html', {'servicios': servicios})

@login_required
def adm_vehiculos(request):
    # Obtener todos los vehículos
    vehiculos = Vehiculo.objects.all()

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            veh_patente = request.POST.get('veh_patente')
            veh_marca = request.POST.get('veh_marca')
            veh_modelo = request.POST.get('veh_modelo')
            veh_anno = request.POST.get('veh_anno')
            veh_img = request.FILES.get('veh_img')

            # Crear y guardar el nuevo vehículo
            nuevo_vehiculo = Vehiculo(
                veh_patente=veh_patente,
                veh_marca=veh_marca,
                veh_modelo=veh_modelo,
                veh_anno=veh_anno,
                veh_img=veh_img,
            )
            nuevo_vehiculo.save()

            vehiculo_data = {
                'veh_patente': nuevo_vehiculo.veh_patente,
                'veh_marca': nuevo_vehiculo.veh_marca,
                'veh_modelo': nuevo_vehiculo.veh_modelo,
                'veh_anno': nuevo_vehiculo.veh_anno,
                'veh_img': nuevo_vehiculo.veh_img.url if nuevo_vehiculo.veh_img else None,
            }
            return JsonResponse(vehiculo_data)

        except Exception as e:
            return JsonResponse({'error': str(e)})

    return render(request, 'admin/adm_vehiculos.html', {'vehiculos': vehiculos})

@csrf_exempt
def add_service(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        ser_desc = request.POST.get('ser_desc')
        ser_prec = request.POST.get('ser_prec')
        ser_durac = request.POST.get('ser_durac')

        # Crear y guardar el nuevo servicio
        servicio = Servicio(
            ser_desc=ser_desc,
            ser_prec=ser_prec,
            ser_durac=ser_durac
        )
        servicio.save()

        servicio_data = {
            'ser_id': servicio.ser_id,
            'ser_desc': servicio.ser_desc,
            'ser_prec': servicio.ser_prec,
            'ser_durac': servicio.ser_durac,
        }
        return JsonResponse(servicio_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
def adm_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'admin/adm_proveedores.html', {'proveedores': proveedores})

@csrf_exempt  # Esto es para desactivar la protección CSRF temporalmente
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

"""_____________________ Carrito _____________________"""

def agregarServicio(request, ser_id):
    carrito= Carrito(request)
    servicio= Servicio.objects.get(ser_id=ser_id)
    carrito.agregar(servicio)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def eliminarServicio(request, ser_id):
    carrito= Carrito(request)
    servicio= Servicio.objects.get(ser_id=ser_id)
    carrito.eliminar(servicio)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def restarServicio(request, ser_id):
    carrito= Carrito(request)
    servicio= Servicio.objects.get(ser_id=ser_id)
    carrito.restar(servicio)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def limpiarCarrito(request):
    carrito= Carrito(request)
    carrito.limpiar()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

"""_____________________ Carrito _____________________"""
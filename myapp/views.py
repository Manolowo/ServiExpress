from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from myapp.utils import render_to_pdf

from .models import UserProfile
from .models import Servicio
from .models import Proveedor
from .models import Vehiculo
from .models import Atencion
from .models import Pedido
from .models import Repuestos
from .models import Inventario


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
            elif rol_description == 'Personal':
                return redirect('per_home')
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
    try:
        user_profile = UserProfile.objects.get(user_id=request.session['user_id'])
        print("User ID from session:", request.session.get('user_id'))
        print("User Profile for current user:", user_profile)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'UserProfile no encontrado'})
    
    return render(request, 'cliente/cli_home.html', {'user_profile': user_profile} )

def cli_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'cliente/cli_servicios.html', {'servicios': servicios})

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

def per_home(request):
    try:
        user_profile = UserProfile.objects.get(user_id=request.session['user_id'])
        print("User ID from session:", request.session.get('user_id'))
        print("User Profile for current user:", user_profile)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'UserProfile no encontrado'})    
    return render(request, 'personal/per_home.html', {'user_profile': user_profile})

def per_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'personal/per_proveedores.html', {'proveedores': proveedores})

def adm_home(request):
    try:
        user_profile = UserProfile.objects.get(user_id=request.session['user_id'])
        print("User ID from session:", request.session.get('user_id'))
        print("User Profile for current user:", user_profile)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'UserProfile no encontrado'})
        
    return render(request, 'admin/adm_home.html', {'user_profile': user_profile})

def adm_users(request):
    users = UserProfile.objects.all()
    return render(request, 'admin/adm_users.html', {'users': users})

def filtered_users(request):
    filter_value = request.GET.get('search', '')
    role_filter = request.GET.get('role_filter', '')

    # Filtrar los usuarios según el valor de búsqueda
    users = UserProfile.objects.filter(Q(user_name__icontains=filter_value) | Q(user_lastname__icontains=filter_value))

    # Aplicar filtro adicional por rol si se proporciona
    if role_filter:
        users = users.filter(rol__rol_description=role_filter)

    user_data = []
    for user in users:
        user_data.append({
            'id': user.user_id,
            'rol_id': user.rol.rol_id,
            'rol_description': user.rol.rol_description,
            'user_name': user.user_name,
            'user_lastname': user.user_lastname,
            'user_mail': user.user_mail,
            'user_fono': user.user_fono,
        })

    return JsonResponse({'users': user_data})

def generate_pdf(request):
    filter_value = request.GET.get('search', '')
    role_filter = request.GET.get('role_filter', '')

    # Filtrar los usuarios según el valor de búsqueda
    users = UserProfile.objects.filter(user_name__icontains=filter_value)

    # Aplicar filtro adicional por rol si se proporciona
    if role_filter:
        users = users.filter(rol__rol_description=role_filter)

    user_data = {'users': users}

    # Utiliza la plantilla adm_users.html para generar el PDF
    template_path = 'admin/adm_users.html'  # Ajusta la ruta según tu estructura de directorios
    pdf = render_to_pdf(template_path, user_data)

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="usuarios.pdf"'
        return response

    return HttpResponse("Error al generar el PDF", status=400)

def adm_atenciones(request):
    users = UserProfile.objects.all()
    atenciones = Atencion.objects.all()
    return render(request, 'admin/adm_atenciones.html', {'users': users , 'atenciones': atenciones})

def facturar_atencion(request, ate_id):
    # Obtén la atención específica o devuelve un 404 si no existe
    atencion = get_object_or_404(Atencion, ate_id=ate_id)

    # Pasa la atención al contexto de la plantilla
    atencion_data = {'atencion': atencion}

    # Utiliza la plantilla específica para la factura
    template_path = 'admin/factura_template.html'
    
    # Usa render_to_pdf para generar el PDF
    pdf = render_to_pdf(template_path, atencion_data)

    if pdf:
        # Devuelve el PDF como una respuesta HTTP
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"factura_atencion_{atencion.ate_id}.pdf"
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response

    return HttpResponse("Error al generar el PDF", status=400)

def adm_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'admin/adm_servicios.html', {'servicios': servicios})

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

@csrf_exempt
def delete_service(request):
    if request.method == 'POST':
        ser_id = request.POST.get('ser_id')
        try:
            servicio = Servicio.objects.get(ser_id=ser_id)
            servicio.delete()
            return JsonResponse({'success': True, 'message': 'Servicio eliminado correctamente'})
        except Servicio.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El servicio no existe'})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

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

def adm_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'admin/adm_proveedores.html', {'proveedores': proveedores})

@csrf_exempt
def add_proveedor(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        pro_nom = request.POST.get('pro_nom')
        pro_mail = request.POST.get('pro_mail')

        # Crear y guardar el nuevo proveedor
        proveedor = Proveedor(
            pro_nom=pro_nom,
            pro_mail=pro_mail
        )
        proveedor.save()

        proveedor_data = {
            'pro_id': proveedor.pro_id,
            'pro_nom': proveedor.pro_nom,
            'pro_mail': proveedor.pro_mail,
        }
        return JsonResponse(proveedor_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
@csrf_exempt
def delete_proveedor(request):
    if request.method == 'POST':
        pro_id = request.POST.get('pro_id')
        try:
            proveedor = Proveedor.objects.get(pro_id=pro_id)
            proveedor.delete()
            return JsonResponse({'success': True, 'message': 'Proveedor eliminado correctamente'})
        except Proveedor.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El proveedor no existe'})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

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

def adm_pedidos(request):
    pedidos = Pedido.objects.all()
    repuestos = Repuestos.objects.all()
    atenciones = Atencion.objects.all()
    users = UserProfile.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, 'admin/adm_pedidos.html', {'proveedores': proveedores, 'pedidos': pedidos,'repuestos': repuestos, 'atenciones': atenciones , 'users': users})

@csrf_exempt
def add_pedido(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        atencion_id = request.POST.get('atencion')
        proveedor_id = request.POST.get('proveedor')
        # Crear el pedido con proveedor
        pedido = Pedido.objects.create(atencion_id=atencion_id, proveedor_id=proveedor_id)

        # Obtener datos de repuestos
        rep_nom = request.POST.getlist('rep-nom')
        rep_marc = request.POST.getlist('rep-marc')
        rep_anno = request.POST.getlist('rep-anno')
        rep_cant = request.POST.getlist('rep-cant')

        # Crear repuestos asociados al pedido
        for i in range(len(rep_nom)):
            Repuestos.objects.create(
                rep_nom=rep_nom[i],
                rep_marc=rep_marc[i],
                rep_anno=rep_anno[i],
                rep_cant=rep_cant[i],
                pedido=pedido
            )

        pedido_data = {
            'ped_id': pedido.ped_id,
            'atencion_id': pedido.atencion.ate_id,
            'ped_est': pedido.ped_est,
            'ped_fecha': pedido.ped_fecha,
        }
        
        return redirect('adm_home')
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
def adm_inv(request):
    inventario = Inventario.objects.all()
    return render(request, 'admin/adm_inv.html', {'inventario': inventario})

def filtered_inventario(request):
    filter_value = request.GET.get('search', '')
    marca_filter = request.GET.get('marca_filter', '')
    anno_filter = request.GET.get('anno_filter', '')

    # Construir la expresión de filtrado
    filter_expr = Q()

    if filter_value:
        filter_expr &= Q(rep_nom__icontains=filter_value)

    if marca_filter:
        filter_expr &= Q(rep_marc__icontains=marca_filter)

    if anno_filter.isdigit():
        filter_expr &= Q(rep_anno=int(anno_filter))

    # Filtrar el inventario según la expresión construida
    inventario = Inventario.objects.filter(filter_expr)

    inventario_data = []
    for item in inventario:
        inventario_data.append({
            'rep_nom': item.rep_nom,
            'rep_marc': item.rep_marc,
            'rep_anno': item.rep_anno,
            'inv_cantTotal': item.inv_cantTotal,
        })

    return JsonResponse({'inventario': inventario_data})

def generate_pdf_inventario(request):
    filter_value = request.GET.get('search', '')
    marca_filter = request.GET.get('marca_filter', '')
    anno_filter = request.GET.get('anno_filter', '')

    # Filtrar el inventario según el valor de búsqueda
    inventario = Inventario.objects.filter(
        rep_nom__icontains=filter_value,
        rep_marc__icontains=marca_filter,
        rep_anno__icontains=anno_filter
    )

    inventario_data = {'inventario': inventario}

    template_path = 'admin/adm_inv.html'  
    pdf = render_to_pdf(template_path, inventario_data)

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="inventario.pdf"'
        return response

    return HttpResponse("Error al generar el PDF", status=400)


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
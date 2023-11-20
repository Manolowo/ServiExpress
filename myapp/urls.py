from django.urls import path
from . import views
from myapp.views import agregarServicio,eliminarServicio,restarServicio,limpiarCarrito

urlpatterns=[
    path('', views.index, name="index"),

    path('login_view/', views.login_view, name='login_view'),
    path('crear_cuenta/', views.crear_cuenta, name='crear_cuenta'),
    
    path('cli_home/', views.cli_home, name='cli_home'),
    path('cli_servicios/', views.cli_servicios, name='cli_servicios'),
    path('cli_vehiculo/', views.cli_vehiculo, name='cli_vehiculo'),
    path('agregar/<int:ser_id>/', agregarServicio, name="Add"),
    path('eliminar/<int:ser_id>/', eliminarServicio, name="Del"),
    path('restar/<int:ser_id>/', restarServicio, name="Sub"),
    path('limpiar/', limpiarCarrito, name="CLS"),


    path('emp_home/', views.emp_home, name='emp_home'),
    
    path('adm_home/', views.adm_home, name='adm_home'),
    path('adm_servicios/', views.adm_servicios, name='adm_servicios'),
    path('add_service/', views.add_service, name='add_service'),
    path('adm_proveedores/', views.adm_proveedores, name='adm_proveedores'),
    path('adm_users/', views.adm_users, name='adm_users'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/', views.delete_user, name='delete_user'),

]
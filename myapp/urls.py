from django.urls import path
from . import views
from myapp.views import agregarServicio,eliminarServicio,restarServicio,limpiarCarrito

urlpatterns=[
    path('', views.index, name="index"),

    path('login_view/', views.login_view, name='login_view'),
    path('crear_cuenta/', views.crear_cuenta, name='crear_cuenta'),
    
    path('cli_home/', views.cli_home, name='cli_home'),
    path('cli_atencion/', views.cli_atencion, name='cli_atencion'),
    path('cli_servicios/', views.cli_servicios, name='cli_servicios'),
    path('cli_vehiculo/', views.cli_vehiculo, name='cli_vehiculo'),
    path('agregar/<int:ser_id>/', agregarServicio, name="Add"),
    path('eliminar/<int:ser_id>/', eliminarServicio, name="Del"),
    path('restar/<int:ser_id>/', restarServicio, name="Sub"),
    path('limpiar/', limpiarCarrito, name="CLS"),

    path('per_home/', views.per_home, name='per_home'),
    path('per_proveedores/', views.per_proveedores, name='per_proveedores'),
    
    path('adm_home/', views.adm_home, name='adm_home'),
    path('adm_atenciones/', views.adm_atenciones, name='adm_atenciones'),
    path('facturar_atencion/<int:ate_id>/', views.facturar_atencion, name='facturar_atencion'),

    path('adm_servicios/', views.adm_servicios, name='adm_servicios'),
    path('add_service/', views.add_service, name='add_service'),
    path('delete_service/', views.delete_service, name='delete_service'),

    path('adm_proveedores/', views.adm_proveedores, name='adm_proveedores'),
    path('add_proveedor/', views.add_proveedor, name='add_proveedor'),
    path('delete_proveedor/', views.delete_proveedor, name='delete_proveedor'),

    path('adm_pedidos/', views.adm_pedidos, name='adm_pedidos'),
    path('add_pedido/', views.add_pedido, name='add_pedido'),
    
    path('adm_inv', views.adm_inv, name='adm_inv'),
    path('filtered_inventario', views.filtered_inventario, name='filtered_inventario'),
    path('generate_pdf_inventario', views.generate_pdf_inventario, name='generate_pdf_inventario'),

    path('adm_users/', views.adm_users, name='adm_users'),
    path('filtered_users/', views.filtered_users, name='filtered_users'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/', views.delete_user, name='delete_user'),

    path('adm_vehiculos', views.adm_vehiculos, name='adm_vehiculos'),

]
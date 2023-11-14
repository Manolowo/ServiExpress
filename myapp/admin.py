from django.contrib import admin

from .models import Rol,UserProfile,Vehiculo,Servicio,Proveedor,Atencion,Pedido,Repuestos,Inventario
# Register your models here.

admin.site.register(Rol)
admin.site.register(UserProfile)
admin.site.register(Vehiculo)
admin.site.register(Servicio)
admin.site.register(Proveedor)
admin.site.register(Atencion)
admin.site.register(Pedido)
admin.site.register(Repuestos)
admin.site.register(Inventario)

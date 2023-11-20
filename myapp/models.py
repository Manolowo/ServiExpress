from django.db import models

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Rol(models.Model):
    rol_id = models.CharField(max_length=3, primary_key=True)
    rol_description = models.CharField(max_length=12)
    
    def __str__(self):
        return self.rol_description

class UserProfile(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=15, null=False)
    user_lastname = models.CharField(max_length=20, null=False)
    user_password = models.CharField(max_length=20, null=False, default="admin")
    user_mail = models.EmailField(null=False)
    user_fono = models.IntegerField(null=False)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_name +' '+ self.user_lastname +' - '+ self.rol.rol_id  

class Vehiculo(models.Model):
    veh_patente= models.CharField(max_length=6, primary_key=True)
    veh_marca= models.CharField(max_length=15, null=False)
    veh_modelo= models.CharField(max_length=25, null=False)
    veh_anno = models.CharField(max_length=4, null=False)
    veh_img = models.ImageField(upload_to='veh_img/', null=True, blank=True)
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.veh_patente
    
class Servicio(models.Model):
    ser_id= models.AutoField(primary_key=True)
    ser_desc= models.CharField(max_length=50, null=False)
    ser_prec= models.IntegerField(null=False)
    ser_durac= models.CharField(max_length=25, null=False)

    def __str__(self):
        return self.ser_desc

class Proveedor(models.Model):
    pro_id= models.AutoField(primary_key=True)
    pro_nom= models.CharField(max_length=20, null=False)
    pro_mail= models.EmailField(null=False)

    def __str__(self):
        return self.pro_nom +' - '+ self.pro_mail

class Atencion(models.Model):
    ate_id = models.AutoField(primary_key=True)
    ate_list = models.CharField(max_length=250, null=False, default=None)
    ate_date = models.DateTimeField()
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=None)

    class Meta:
        unique_together = ['ate_date']
    
    def clean(self):
        # Validar que la fecha y hora no sea en el pasado
        if self.ate_date < timezone.now():
            raise ValidationError('La fecha y hora de la atención no pueden ser en el pasado.')
        # Resto de la validación
        super(Atencion, self).clean()

class Pedido(models.Model):
    estados = (
        ('En Proceso','En Proceso'),
        ('Solicitado', 'Solicitado'),
        ('Cancelado', 'Cancelado'),
        ('Entregado', 'Entregado'),
    )
    ped_id = models.AutoField(primary_key=True)
    ped_est = models.CharField(max_length=12, choices= estados, default='En Proceso')
    ped_fecha = models.DateTimeField(auto_now_add=True, null=False)
    atencion = models.ForeignKey(Atencion, on_delete=models.SET_NULL, null=True)

class Repuestos(models.Model):
    rep_id = models.AutoField(primary_key=True)
    rep_nom = models.CharField(max_length=50, null=False)
    rep_marc = models.CharField(max_length=25, default='Generica')
    rep_anno = models.CharField(max_length=4, null=False)
    rep_cant= models.IntegerField(default= 1, null=False)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)

class Inventario(models.Model):
    rep_nom = models.CharField(max_length=50)
    rep_marc = models.CharField(max_length=25)
    rep_anno = models.DateField()
    inv_cantTotal = models.IntegerField(default=0)

@receiver(post_save, sender=Repuestos)
def actualizar_inventario(sender, instance, created, **kwargs):
    if created:
        inventario, _ = Inventario.objects.get_or_create(
            rep_nom=instance.rep_nom,
            rep_marc=instance.rep_marc,
            rep_anno=instance.rep_anno,
        )
        inventario.inv_cantTotal += instance.rep_cant
        inventario.save()
    else:
        inventario = Inventario.objects.get(
            rep_nom=instance.rep_nom,
            rep_marc=instance.rep_marc,
            rep_anno=instance.rep_anno,
        )
        inventario.inv_cantTotal += instance.rep_cant
        inventario.save()
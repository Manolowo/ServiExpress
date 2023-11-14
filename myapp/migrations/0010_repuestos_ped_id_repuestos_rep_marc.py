# Generated by Django 4.2.6 on 2023-11-14 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_atencion_ate_date_atencion_ate_list_atencion_user_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='repuestos',
            name='ped_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.pedido'),
        ),
        migrations.AddField(
            model_name='repuestos',
            name='rep_marc',
            field=models.CharField(default='Generica', max_length=25),
        ),
    ]

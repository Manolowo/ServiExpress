# Generated by Django 4.2.6 on 2023-12-09 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_alter_inventario_rep_anno_alter_repuestos_rep_anno'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='proveedor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.proveedor'),
        ),
    ]

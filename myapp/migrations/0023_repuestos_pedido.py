# Generated by Django 4.2.6 on 2023-12-09 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_remove_repuestos_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='repuestos',
            name='pedido',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.pedido'),
        ),
    ]

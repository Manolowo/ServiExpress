# Generated by Django 4.2.6 on 2023-11-14 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_proveedor_pro_id_alter_repuestos_rep_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rep_nom', models.CharField(max_length=50)),
                ('rep_marc', models.CharField(max_length=25)),
                ('rep_anno', models.DateField()),
                ('inv_cantTotal', models.IntegerField(default=0)),
            ],
        ),
        migrations.RenameModel(
            old_name='User',
            new_name='UserProfile',
        ),
        migrations.AddField(
            model_name='repuestos',
            name='rep_cant',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='atencion',
            name='ate_date',
            field=models.DateTimeField(),
        ),
    ]

# Generated by Django 4.2.6 on 2023-11-05 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_usuario_id_usuario'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]

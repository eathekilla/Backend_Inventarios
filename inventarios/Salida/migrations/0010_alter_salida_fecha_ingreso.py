# Generated by Django 4.2.3 on 2023-08-24 15:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salida', '0009_alter_salida_fecha_ingreso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salida',
            name='fecha_ingreso',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 24, 10, 44, 28, 769326)),
        ),
    ]
# Generated by Django 4.2.3 on 2023-11-08 16:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Entrada', '0043_alter_entrada_fecha_vencimiento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='fecha_vencimiento',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 8, 11, 20, 29, 926401)),
        ),
        migrations.AlterField(
            model_name='historicalentrada',
            name='fecha_vencimiento',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 8, 11, 20, 29, 926401)),
        ),
    ]

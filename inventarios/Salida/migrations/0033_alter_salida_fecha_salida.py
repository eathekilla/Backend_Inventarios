# Generated by Django 4.2.3 on 2023-10-26 15:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salida', '0032_alter_salida_fecha_salida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salida',
            name='fecha_salida',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 26, 10, 12, 16, 23657)),
        ),
    ]

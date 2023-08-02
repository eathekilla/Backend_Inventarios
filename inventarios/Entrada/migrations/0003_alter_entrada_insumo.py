# Generated by Django 4.2.3 on 2023-08-01 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Insumo', '0002_remove_insumo_grupo_insumo_certificacion_and_more'),
        ('Entrada', '0002_alter_entrada_a_finca_alter_entrada_de_finca_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='insumo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entrada_insumo', to='Insumo.insumo'),
        ),
    ]
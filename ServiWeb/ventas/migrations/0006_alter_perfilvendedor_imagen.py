# Generated by Django 3.2.8 on 2023-11-12 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0005_remove_arriendos_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilvendedor',
            name='imagen',
            field=models.ImageField(blank=True, default='vendedores.png', null=True, upload_to='vendedorperfil'),
        ),
    ]
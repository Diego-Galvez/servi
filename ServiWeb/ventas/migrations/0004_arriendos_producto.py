# Generated by Django 3.2.8 on 2023-11-11 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0003_producto_categorias'),
    ]

    operations = [
        migrations.AddField(
            model_name='arriendos',
            name='producto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ventas.producto'),
            preserve_default=False,
        ),
    ]

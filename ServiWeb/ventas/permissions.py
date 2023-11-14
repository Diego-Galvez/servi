from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from ventas.models import Cliente, Producto

# Asignar permisos al grupo "cliente"
cliente_content_type = ContentType.objects.get_for_model(Cliente)
Permission.objects.get_or_create(codename='view_cliente_profile', name='View Cliente Profile', content_type=cliente_content_type)
Permission.objects.get_or_create(codename='add_arriendos', name='Add Arriendos', content_type=cliente_content_type)
Permission.objects.get_or_create(codename='edit_arriendos', name='Edit Arriendos', content_type=cliente_content_type)

# Asignar permisos al grupo "vendedor"
vendedor_content_type = ContentType.objects.get_for_model(Producto)
Permission.objects.get_or_create(codename='view_ventas', name='View Ventas', content_type=vendedor_content_type)
Permission.objects.get_or_create(codename='add_producto', name='Add Producto', content_type=vendedor_content_type)
Permission.objects.get_or_create(codename='edit_producto', name='Edit Producto', content_type=vendedor_content_type)
Permission.objects.get_or_create(codename='add_venta', name='Add Venta', content_type=vendedor_content_type)


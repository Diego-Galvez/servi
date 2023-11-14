from django.db import models
from django.forms import model_to_dict
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User




# Create your models here.
class Cliente(models.Model):
    rut = models.CharField(max_length=200, null=True, blank=True)
    nombre = models.CharField(max_length=200, null=True, blank=True)
    apellido = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    empresa = models.CharField(max_length=200, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name='clientes'
        verbose_name_plural='clientes'
        
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=200, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=200, null=True, blank=True)
    descripcion = models.TextField(max_length=255, null=False)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)
    precio = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    cantidad = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    categorias = models.CharField(max_length=100)

    class Meta:
        verbose_name='producto'
        verbose_name_plural='productos'
        order_with_respect_to = 'descripcion'
        
    def __str__(self):
        return self.descripcion
    
class Egreso(models.Model):
    fecha_pedido = models.DateField(max_length=255)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL , null=True , related_name='clientee')
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pagado = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    comentarios = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    ticket = models.BooleanField(default=True)
    desglosar = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=True , null=True)

    class Meta:
        verbose_name='egreso'
        verbose_name_plural = 'egresos'
        order_with_respect_to = 'fecha_pedido'
    
    def __str__(self):
        return str(self.id)
   
class ProductosEgreso(models.Model):
    egreso = models.ForeignKey(Egreso, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2 , null=False)
    precio = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    iva = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    created = models.DateTimeField(auto_now_add=True)
    entregado = models.BooleanField(default=True)
    devolucion = models.BooleanField(default=False)
    categorias = models.CharField(max_length=100)

    class Meta:
        verbose_name='producto egreso'
        verbose_name_plural = 'productos egreso'
        order_with_respect_to = 'created'
    
    def __str__(self):
        return self.producto
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['created'])
        return item

class Empresa(models.Model):
    rut = models.CharField(max_length=200, null=True, blank=True)
    nombre = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    empresa = models.CharField(max_length=200, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name='empresa'
        verbose_name_plural='Empresas'
        
    def __str__(self):
        return self.nombre

ESTADO_CHOICES_CONTACTMESSAGE = (
    ('Pendiente', 'Pendiente'),
    ('Contactado', 'Contactado'),
)
class ContactMessage(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    telefono_contacto = models.CharField(max_length=15, blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES_CONTACTMESSAGE, default='Pendiente')

    def __str__(self):
        return self.nombre
    
class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    precio_envio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name='comunas'
        verbose_name_plural='comunas'

    def __str__(self):
        return self.nombre

ESTADO_CHOICES_ARRIENDO = (
    ('Pendiente', 'Pendiente'),
    ('Realizado', 'Realizado'),
    ('Cancelado', 'Cancelado'),
)
class Arriendo(models.Model):
    fecha = models.DateField()
    id_cliente = models.IntegerField()
    cliente = models.CharField(max_length=100)
    comentarios = models.TextField()
    modoentrega = models.CharField(max_length=50)
    nombre_herramienta = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2) 
    comuna = models.CharField(max_length=255)  
    precio_envio = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES_ARRIENDO, default='Pendiente')

ESTADO_CHOICES_ARRIENDO_CLIENTE = (
    ('Pendiente', 'Pendiente'),
    ('Realizado', 'Realizado'),
    ('Cancelado', 'Cancelado'),
)
ESTADO_CHOICES_ARRIENDO_PEDIDO = (
    ('No', 'No'),
    ('Si', 'Si'),
)
class Arriendos(models.Model):
    fecha = models.DateField()
    user = models.CharField(max_length=150)
    rut = models.CharField(max_length=20)
    nombre_cliente = models.CharField(max_length=255)
    comentarios = models.TextField()
    modoentrega = models.CharField(max_length=50)
    nombre_herramienta = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2) 
    comuna = models.CharField(max_length=255)  
    precio_envio = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES_ARRIENDO_CLIENTE, default='Pendiente')
    pedido = models.CharField(max_length=20, choices=ESTADO_CHOICES_ARRIENDO_PEDIDO, default='No')


class PerfilCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='clienteperfil', null=True, blank=True,default='users.png')
    rut = models.CharField(max_length=20)
    telefono_contacto = models.CharField(max_length=15)
    empresa = models.CharField(max_length=100)
    nombre_completo = models.CharField(max_length=255)  
    correo = models.EmailField() 

    def _str_(self):
        return self.user.username
    
class PerfilVendedor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='vendedorperfil', null=True, blank=True,default='vendedores.png')
    rut = models.CharField(max_length=20)
    telefono_contacto = models.CharField(max_length=15)
    empresa = models.CharField(max_length=100)
    nombre_completo = models.CharField(max_length=255)  
    correo = models.EmailField() 

    def _str_(self):
        return self.user.username

cliente_group, created = Group.objects.get_or_create(name='cliente')
vendedor_group, created = Group.objects.get_or_create(name='vendedor')

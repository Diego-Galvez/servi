from django import forms
from ventas.models import Cliente, Producto, ContactMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comuna, Producto, Cliente, PerfilCliente, PerfilVendedor


class AddClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('rut', 'nombre', 'apellido', 'telefono', 'email', 'empresa', 'direccion')
        labels = {
            'rut': 'Rut Cliente: ',
            'nombre': 'Nombre Cliente: ',
            'apellido': 'Apellido Cliente: ',
            'telefono': 'Telefono Cliente: ',
            'email': 'Email Cliente: ',
            'empresa': 'Empresa Cliente: ',
            'direccion': 'Direccion Empresa: ',
        }

class EditarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('rut', 'nombre', 'apellido', 'telefono', 'email', 'empresa', 'direccion')
        labels = {
            'rut': 'Rut Cliente: ',
            'nombre': 'Nombre Cliente: ',
            'apellido': 'Apellido Cliente: ',
            'telefono': 'Telefono Cliente: ',
            'email': 'Email Cliente: ',
            'empresa': 'Empresa Cliente: ',
            'direccion': 'Direccion Empresa: ',
        }
        widgets = {
            'rut': forms.TextInput(attrs={'type': 'text', 'id': 'rut_editar'}),
            'nombre': forms.TextInput(attrs={'id': 'nombre_editar'}),
            'apellido': forms.TextInput(attrs={'id': 'apellido_editar'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono_editar'}),
            'email': forms.TextInput(attrs={'id': 'email_editar'}),
            'empresa': forms.TextInput(attrs={'id': 'empresa_editar' }),
            'direccion': forms.TextInput(attrs={'id': 'direccion_editar'}),
        }

class AddProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('codigo', 'nombre', 'descripcion', 'imagen', 'precio', 'cantidad', 'categorias')
        labels = {
            'codigo': 'Codigo Producto: ',
            'nombre': 'Nombre Producto: ',
            'descripcion': 'Descripcion Producto: ',
            'imagen': 'Imagen Producto: ',
            'precio': 'Precio Producto $: ',
            'cantidad': 'Cantidad Producto: ',
            'categorias': 'Categoria',

        }

class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('codigo', 'nombre', 'descripcion', 'imagen', 'precio', 'cantidad', 'categorias')
        labels = {
            'codigo': 'Codigo Producto: ',
            'nombre': 'Nombre Producto: ',
            'descripcion': 'Descripcion Producto: ',
            'imagen': 'Imagen Producto: ',
            'precio': 'Precio Producto $: ',
            'cantidad': 'Cantidad Producto: ',
            'categorias': 'Categoria',

        }
        widgets = {
            'codigo': forms.TextInput(attrs={'type': 'text', 'id': 'codigo_editar'}),
            'nombre': forms.TextInput(attrs={'id': 'nombre_editar'}),
            'descripcion': forms.TextInput(attrs={'id': 'descripcion_editar'}),
            'precio': forms.TextInput(attrs={'id': 'precio_editar'}),
            'cantidad': forms.TextInput(attrs={'id': 'cantidad_editar' }),
            'categorias': forms.TextInput(attrs={'id': 'categorias_editar' }),

        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['nombre', 'email', 'mensaje', 'telefono_contacto']
    telefono_contacto = forms.CharField(max_length=15, required=False, label="Teléfono de contacto")

class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model = User   
        fields = ['username', "first_name", "last_name", "email", "password1", "password2"]
        emprlabels = {
            'rut': 'Rut Cliente: ',
            'nombre': 'Nombre Cliente: ',
            'apellido': 'Apellido Cliente: ',
            'telefono': 'Telefono Cliente: ',
            'email': 'Email Cliente: ',
            'empresa': 'Empresa Cliente: ',
            'direccion': 'Direccion Empresa: ',
        }

class ArriendoForm(forms.Form):
    direccion = forms.CharField(max_length=100)
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all())
    empresa = forms.CharField(max_length=100)
    productos = forms.ModelMultipleChoiceField(queryset=Producto.objects.all())
    cantidad_producto = forms.IntegerField(min_value=1, initial=1)  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna'].label_from_instance = lambda obj: obj.nombre  

class ComunaForm(forms.ModelForm):
    class Meta:
        model = Comuna
        fields = ('nombre', 'precio_envio')
        labels = {
            'comuna': 'Nombre Comuna', 
            'precio_envio': 'Precio Envío'
        }

class EditComunaForm(forms.ModelForm):
    class Meta:
        model = Comuna
        fields = ('nombre', 'precio_envio')
        labels = {
            'comuna': 'Nombre Comuna', 
            'precio_envio': 'Precio Envío'
        }
        
class RegistroClienteForm(UserCreationForm):
    tipo = forms.ChoiceField(choices=[('cliente', 'Cliente')])

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'tipo']

class RegistroVendedorForm(UserCreationForm):
    nombre_empresa = forms.CharField(max_length=100, required=True)
    tipo = forms.ChoiceField(choices=[('cliente', 'Cliente'), ('vendedor', 'Vendedor')])

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nombre_empresa', 'tipo']  

class PerfilClienteForm(forms.ModelForm):
    class Meta:
        model = PerfilCliente
        l = PerfilCliente
        fields = ['rut', 'telefono_contacto', 'empresa','imagen']

class PerfilVendedorForm(forms.ModelForm):
    class Meta:
        model = PerfilVendedor
        fields = ['rut', 'telefono_contacto', 'empresa','imagen']
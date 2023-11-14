from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ventas.models import Cliente, Producto, Empresa
from .models import Comuna

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido', 'telefono', 'empresa')
    search_fields = ['nombre']
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Cliente, ClienteAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'descripcion', 'precio')
    search_fields = ['nombre']
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Producto, ProductoAdmin)

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'telefono', 'email', 'empresa', 'direccion')
    search_fields = ['nombre']
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Empresa, EmpresaAdmin)


admin.site.register(Comuna)





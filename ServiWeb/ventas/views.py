from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Producto, Egreso, ProductosEgreso, Producto, Comuna, Arriendo, Arriendos, PerfilCliente, PerfilVendedor
from .forms import AddClienteForm, EditarClienteForm, AddProductoForm, EditarProductoForm, ContactForm, ComunaForm, EditComunaForm, RegistroClienteForm, PerfilClienteForm, PerfilVendedorForm
from django.contrib import messages
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from weasyprint.text.fonts import FontConfiguration
from django.template.loader import get_template
from weasyprint import HTML, CSS
from django.conf import settings
import os
from .models import *
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
import json
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView
from django.contrib.auth import get_user
import logging
from reportlab.pdfgen import canvas
from django.templatetags.static import static
from django.conf import settings
from xhtml2pdf import pisa
from django.db.models import Count
from django.views.generic import TemplateView
from datetime import datetime as dt
from itertools import groupby
from django.db.models.functions import TruncMonth
from itertools import groupby
from django.contrib.auth.mixins import UserPassesTestMixin
import sweetify








#home
def home_view(request):
    return render(request,'home/inicio.html')

def inicio_view(request):
    return render(request,'home/inicio.html')

def quienes_view(request):
    return render(request,'home/quienessomos.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'home/contact.html', {'form': form})

def catalogo(request):
    productos = Producto.objects.all().order_by('categorias', 'descripcion')

    categorias_productos = {}
    for key, group in groupby(productos, key=lambda x: x.categorias):
        categorias_productos[key] = list(group)

    return render(request, 'home/catalogo.html', {'categorias_productos': categorias_productos})


#sesion usuarios
def es_cliente(user):
    return user.groups.filter(name='cliente').exists()

def es_vendedor(user):
    return user.groups.filter(name='vendedor').exists()

def registrar_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            tipo = form.cleaned_data['tipo']
            if tipo == 'cliente':
                grupo_cliente = Group.objects.get(name='cliente')
                user.groups.add(grupo_cliente)
                perfil_cliente, created = PerfilCliente.objects.get_or_create(user=user)
            login(request, user)  
            return redirect('perfilcliente')
    else:
        form = RegistroClienteForm()
    return render(request, 'registration/registrocliente.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')  
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("Usuario autenticado:", user)
            login(request, user)

            if user.groups.filter(name='cliente').exists():
                print("Usuario es un cliente con permisos")
                return redirect('perfilcliente')  
            if user.groups.filter(name='vendedor').exists():
                print("Usuario es un vendedor con permisos")
                return redirect('perfilvendedor')  
        else:
            sweetify.error(request, 'Credenciales incorrectas')    
            return redirect('login')



#cliente
@user_passes_test(es_cliente)
def cliente_profile_view(request):
    nombre_cliente = request.user.first_name

    context = {
        'nombre_cliente': nombre_cliente,
    }

    return render(request, 'cliente/perfilcliente.html', context)

@user_passes_test(es_cliente)
def arriendos_view(request):
    user = request.user
    productos = Producto.objects.all()
    return render(request,'cliente/arriendos.html', {'productos': productos})

@user_passes_test(es_cliente)
def add_arriendos(request):
    usuario = get_user(request)
    context = {
        'usuario': usuario,
        'productos_lista': Producto.objects.all(),
        'comunas_lista': Comuna.objects.all(),
    }
    return render(request, 'cliente/add_arriendos.html', context)

class AddArriendos(ListView):
    template_name = 'cliente/add_arriendos.html'
    model = Arriendos
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='cliente').exists()

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            fecha = request.POST.get('fecha')
            comentarios = request.POST.get('comentarios')
            modoentrega = request.POST.get('modo_entrega')
            productos = json.loads(request.POST.get('productos'))
            comuna_nombre = request.POST.get('comuna_nombre')
            precio_envio = request.POST.get('precio_envio')
            total = request.POST.get('total')
            rut = request.POST.get('rut')  
            nombre_cliente = request.POST.get('nombre_cliente')  

            for producto in productos:
                nombre_herramienta = producto['nombre']
                cantidad = producto['cantidad']
                subtotal = producto['subtotal']

                arriendo = Arriendos(
                    fecha=fecha,
                    user=request.user.username,
                    comentarios=comentarios,
                    nombre_herramienta=nombre_herramienta,
                    cantidad=cantidad,
                    subtotal=subtotal,
                    comuna=comuna_nombre,
                    precio_envio=precio_envio,
                    total=total,
                    modoentrega=modoentrega,
                    rut=rut,  
                    nombre_cliente=nombre_cliente  
                )
                arriendo.save()

            data['message'] = 'Arriendo realizado con éxito.'
            data['arriendo_id'] = arriendo.id
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            perfil_cliente = PerfilCliente.objects.get(user=self.request.user)
            context['rut_cliente'] = perfil_cliente.rut
            context['nombre_completo_cliente'] = perfil_cliente.nombre_completo
        except PerfilCliente.DoesNotExist:
            context['rut_cliente'] = ""
            context['nombre_completo_cliente'] = ""
        context['user'] = self.request.user
        context['productos_lista'] = Producto.objects.all()
        context['comunas_lista'] = Comuna.objects.all()
        return context

@user_passes_test(es_cliente)
def informacion(request):
    return render(request, 'cliente/informacion.html')

@user_passes_test(es_cliente) 
def perfilcliente(request):
    if request.user.is_authenticated:
        user = request.user
        perfil, created = PerfilCliente.objects.get_or_create(user=user)
        perfil_form = PerfilClienteForm(instance=perfil)

        if request.method == 'POST':
            perfil_form = PerfilClienteForm(request.POST, request.FILES, instance=perfil) 
            if perfil_form.is_valid():
                perfil = perfil_form.save(commit=False)
                perfil.user = user
                nombre_completo = f"{user.first_name} {user.last_name}"
                perfil.nombre_completo = nombre_completo
                perfil.correo = user.email
                perfil.imagen = request.FILES.get('perfilimg')
                perfil.save()

        return render(request, 'cliente/perfil.html', {'user': user, 'form': perfil_form})
    else:
        return redirect('login')

@user_passes_test(es_cliente)
def lista_arriendos(request):
    user = request.user
    ventas_arriendos = Arriendos.objects.filter(user=user)

    if request.GET.get('pdf'):
        for arriendo in ventas_arriendos:
            pdf_response = descargar_pdf(arriendo)
            if pdf_response.status_code != 200:
                return pdf_response

        return HttpResponse('PDFs generados exitosamente', status=200)

    return render(request, 'cliente/lista_arriendos.html', {'ventas_arriendos': ventas_arriendos})

@user_passes_test(es_cliente)
def arriendos_pendientes(request):
    user = request.user
    ventas_arriendos = Arriendos.objects.filter(user=user, estado='Pendiente')

    if request.GET.get('pdf'):
        for arriendo in ventas_arriendos:
            pdf_response = descargar_pdf(arriendo)
            if pdf_response.status_code != 200:
                return pdf_response

        return HttpResponse('PDFs generados exitosamente', status=200)
    return render(request, 'cliente/pedidoPendiente.html', {'ventas_arriendos': ventas_arriendos})

@user_passes_test(es_cliente)
def arriendos_realizados(request):
    user = request.user
    ventas_arriendos = Arriendos.objects.filter(user=user, estado='Realizado')

    if request.GET.get('pdf'):
        for arriendo in ventas_arriendos:
            pdf_response = descargar_pdf(arriendo)
            if pdf_response.status_code != 200:
                return pdf_response

        return HttpResponse('PDFs generados exitosamente', status=200)
    return render(request, 'cliente/pedidoRealizado.html', {'ventas_arriendos': ventas_arriendos})

@user_passes_test(es_cliente)
def arriendos_cancelados(request):
    user = request.user
    ventas_arriendos = Arriendos.objects.filter(user=user, estado='Cancelado')

    if request.GET.get('pdf'):
        for arriendo in ventas_arriendos:
            pdf_response = descargar_pdf(arriendo)
            if pdf_response.status_code != 200:
                return pdf_response

        return HttpResponse('PDFs generados exitosamente', status=200)
    return render(request, 'cliente/pedidoCancelado.html', {'ventas_arriendos': ventas_arriendos})

@user_passes_test(es_cliente)
def descargar_pdf(request, arriendo_id):
    arriendo = Arriendos.objects.get(id=arriendo_id)

    template_path = 'cliente/ticket.html'
    context = {'arriendo': arriendo}
    
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="arriendo_{arriendo.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

@user_passes_test(es_cliente)
def cancelar_pedido(request):
    if request.method == 'POST':
        id_pedido = request.POST.get('id_pedido')
        pedido = request.POST.get('pedido')

        try:
            arriendo = Arriendos.objects.get(id=id_pedido)
            arriendo.pedido = pedido
            arriendo.save()

            return JsonResponse({'success': True})
        except Arriendos.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Pedido no encontrado'})
    return JsonResponse({'success': False, 'error': 'Solicitud incorrecta'})

@user_passes_test(es_cliente)
def actualizar_pedido(request):
    if request.method == 'POST':
        id_pedido = request.POST.get('id_pedido')
        estado_pedido = request.POST.get('estado_pedido')

        try:
            arriendo = Arriendos.objects.get(id=id_pedido)

            if arriendo.pedido == "Si":
                return JsonResponse({'success': False, 'error': 'No se puede cambiar el estado.'})

            arriendo.pedido = estado_pedido
            arriendo.save()

            return JsonResponse({'success': True})
        except Arriendos.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Pedido no encontrado'})
    return JsonResponse({'success': False, 'error': 'Solicitud incorrecta'})

@user_passes_test(es_cliente)
def catalogocliente(request):
    productos = Producto.objects.all().order_by('categorias', 'descripcion')

    categorias_productos = {}
    for key, group in groupby(productos, key=lambda x: x.categorias):
        categorias_productos[key] = list(group)

    return render(request, 'cliente/catalogo.html', {'categorias_productos': categorias_productos})



#vendedor
@user_passes_test(es_vendedor)
def ventas_view(request):
    ventas_arriendos = Arriendo.objects.all()  
    context = {
        'ventas_arriendos': ventas_arriendos
    }
    return render(request,'vendedor/ventas.html', context)

@user_passes_test(es_vendedor)
def clientes_view(request):
    clientes = Cliente.objects.all()
    form_personal = AddClienteForm()
    form_editar = EditarClienteForm()
    context = {
        'clientes': clientes,
        'form_personal': form_personal,
        'form_editar': form_editar
    }
    return render(request,'vendedor/clientes.html', context)

@user_passes_test(es_vendedor)
def add_cliente_view(request):
    #print("Guardar Cliente")
    if request.POST:
        form = AddClienteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
            except:
                messages(request, "Error al guardar cliente")
                return redirect('Clientes')
        
    return redirect('Clientes')

@user_passes_test(es_vendedor)
def edit_cliente_view(request):
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_editar'))
        form = EditarClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            try:
                form.save()
            except:
                messages(request, "Error al editar cliente")
            
    return redirect('Clientes')

@user_passes_test(es_vendedor)
def delete_cliente_view(request):
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_eliminar'))
        cliente.delete()
    return redirect('Clientes')

@user_passes_test(es_vendedor)
def productos_view(request):
    productos = Producto.objects.all()
    form_add = AddProductoForm()
    form_editar = EditarProductoForm()
    context = {
        'productos': productos,
        'form_add': form_add,
        'form_editar': form_editar
    }
    return render(request,'vendedor/productos.html', context)

@user_passes_test(es_vendedor)
def add_producto_view(request):
    if request.POST:
        form = AddProductoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
            except:
                messages(request, "Error al guardar el producto")
                return redirect('Productos')
        
    return redirect('Productos')

@user_passes_test(es_vendedor)
def edit_producto_view(request):
    if request.POST:
        producto = Producto.objects.get(pk=request.POST.get('id_producto_editar'))
        form = EditarProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            try:
                form.save()
            except:
                messages(request, "Error al editar producto")
            
    return redirect('Productos')

@user_passes_test(es_vendedor)
def delete_producto_view(request):
    if request.POST:
        producto = Producto.objects.get(pk=request.POST.get('id_producto_eliminar'))
        producto.delete()
    return redirect('Productos')

class add_ventas(ListView):
    template_name = 'vendedor/add_ventas.html'
    model = Arriendo

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='vendedor').exists()

    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request,*ars, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(descripcion__icontains=request.POST["term"])[0:10]:
                    item = i.toJSON()
                    item['value'] = i.descripcion
                    data.append(item)
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data,safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos_lista'] = Producto.objects.all()
        context['clientes_lista'] = Cliente.objects.all()
        context['comunas_lista'] = Comuna.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            fecha = request.POST.get('fecha')
            id_cliente = request.POST.get('id_cliente')
            cliente = request.POST.get('cliente')
            comentarios = request.POST.get('comentarios')
            modoentrega = request.POST.get('modo_entrega')
            productos = json.loads(request.POST.get('productos'))
            comuna_nombre = request.POST.get('comuna_nombre')
            precio_envio = request.POST.get('precio_envio')
            total = request.POST.get('total')

            for producto in productos:
                nombre_herramienta = producto['nombre']
                cantidad = producto['cantidad']
                subtotal = producto['subtotal']

                arriendo = Arriendo(
                    fecha=fecha,
                    id_cliente=id_cliente,
                    modoentrega=modoentrega,
                    cliente=cliente,
                    comentarios=comentarios,
                    nombre_herramienta=nombre_herramienta,
                    cantidad=cantidad,
                    subtotal=subtotal,
                    comuna=comuna_nombre, 
                    precio_envio=precio_envio,
                    total=total
                )
                arriendo.save()


            data['message'] = 'Arriendo realizado con éxito.'
            data['arriendo_id'] = arriendo.id
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
    
class ListaProductosView(ListView):
    model = Producto
    template_name = 'vendedor/herramientas.html' 
    context_object_name = 'productos'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='vendedor').exists()

@user_passes_test(es_vendedor)
def export_pdf_view(request, id, iva):
    template = get_template("ticket.html")
    subtotal = 0 
    iva_suma = 0 

    venta = Egreso.objects.get(pk=float(id))
    datos = ProductosEgreso.objects.filter(egreso=venta)
    for i in datos:
        subtotal = subtotal + float(i.subtotal)
        iva_suma = iva_suma + float(i.iva)

    empresa = "Mi empresa S.A. De C.V"
    context ={
        'num_ticket': id,
        'iva': iva,
        'fecha': venta.fecha_pedido,
        'cliente': venta.cliente.nombre,
        'items': datos, 
        'total': venta.total, 
        'empresa': empresa,
        'comentarios': venta.comentarios,
        'subtotal': subtotal,
        'iva_suma': iva_suma,
    }
    html_template = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; ticket.pdf"
    css_url = os.path.join(settings.BASE_DIR,'index\static\index\css/bootstrap.min.css')
   
    font_config = FontConfiguration()
    HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(target=response, font_config=font_config,stylesheets=[CSS(css_url)])

    return response

@user_passes_test(es_vendedor)
def sesion_view(request):
    return render(request,'vendedor/sesion.html')

@user_passes_test(es_vendedor)
def vendedor_profile_view(request):
    nombre_vendedor = request.user.first_name

    context = {
        'nombre_vendedor': nombre_vendedor,
    }

    return render(request, 'vendedor/ventas.html', context)

@user_passes_test(es_vendedor)
def informa(request):
    return render(request, 'vendedor/informa.html')

@user_passes_test(es_vendedor)
def realizar_arriendo(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        id_cliente = request.POST.get('id_cliente')
        cliente = request.POST.get('cliente')
        modoentrega = request.POST.get('modo_entrega')
        comentarios = request.POST.get('comentarios')
        productos = json.loads(request.POST.get('productos'))

        for producto in productos:
            nombre_herramienta = producto['nombre']
            cantidad = producto['cantidad']
            total = producto['subtotal']

            arriendo = Arriendo(
                fecha=fecha,
                id_cliente=id_cliente,
                modoentrega=modoentrega,
                cliente=cliente,
                comentarios=comentarios,
                nombre_herramienta=nombre_herramienta,
                cantidad=cantidad,
        )
        arriendo.save()

        return HttpResponse(json.dumps({'message': 'Arriendo realizado con éxito.'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error': 'No se recibió una solicitud POST válida.'}), content_type="application/json")

@user_passes_test(es_vendedor)
def pedidos(request):
    ventas_arriendos = Arriendo.objects.all()
    if request.GET.get('pdf'):
        for arriendo in ventas_arriendos:
            pdf_response = generar_pdf_vendedor(arriendo)
            if pdf_response.status_code != 200:
                return pdf_response

        return HttpResponse('PDFs generados exitosamente', status=200)

    return render(request, 'vendedor/pedidos.html', {'ventas_arriendos': ventas_arriendos})

@user_passes_test(es_vendedor)
def pedidos_vendedor_pendiente(request):
    ventas_arriendos = Arriendo.objects.filter(estado='Pendiente')
    if request.GET.get('pdf'):
        for arriendo in ventas_arriendos:
            pdf_response = generar_pdf_vendedor(arriendo)
            if pdf_response.status_code != 200:
                return pdf_response

        return HttpResponse('PDFs generados exitosamente', status=200)

    return render(request, 'vendedor/pedidos.html', {'ventas_arriendos': ventas_arriendos})

@user_passes_test(es_vendedor)
def pedidos_vendedor_cancelado(request):
    ventas_arriendos = Arriendo.objects.filter(estado='Cancelado')
    if request.GET.get('pdf'):
        for arriendo in ventas_arriendos:
            pdf_response = generar_pdf_vendedor(arriendo)
            if pdf_response.status_code != 200:
                return pdf_response

        return HttpResponse('PDFs generados exitosamente', status=200)

    return render(request, 'vendedor/pedidos.html', {'ventas_arriendos': ventas_arriendos})

@user_passes_test(es_vendedor)
def pedidos_vendedor_realizado(request):
    ventas_arriendos = Arriendo.objects.filter(estado='Realizado')
    if request.GET.get('pdf'):
        for arriendo in ventas_arriendos:
            pdf_response = generar_pdf_vendedor(arriendo)
            if pdf_response.status_code != 200:
                return pdf_response

        return HttpResponse('PDFs generados exitosamente', status=200)

    return render(request, 'vendedor/pedidos.html', {'ventas_arriendos': ventas_arriendos})

@user_passes_test(es_vendedor)
def generar_pdf_vendedor(request, arriendo_id=None):
    arriendo = get_object_or_404(Arriendo, id=arriendo_id)

    template_path = 'vendedor/ticket.html'
    context = {'arriendo': arriendo}
    
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="arriendo_{arriendo.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

@user_passes_test(es_vendedor)
def mostrar_contactos(request):
    contactos = ContactMessage.objects.all()
    return render(request, 'vendedor/contactanos.html', {'contactos': contactos})

@user_passes_test(es_vendedor)
def eliminar_arriendo(request):
    if request.method == 'POST':
        id_arriendo = request.POST.get('id_arriendo', None)
        if id_arriendo:
            try:
                arriendo = Arriendo.objects.get(id=id_arriendo)
                arriendo.delete()
                return JsonResponse({'success': True})
            except Arriendo.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Arriendo no encontrado'})
        else:
            return JsonResponse({'success': False, 'error': 'ID de arriendo no proporcionado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@user_passes_test(es_vendedor)
def comunas_view(request):
    comunas = Comuna.objects.all()
    form_comuna = ComunaForm()
    form_editar_comuna = EditComunaForm()
    context = {
        'comunas': comunas,
        'form_comuna': form_comuna,
        'form_editar_comuna': form_editar_comuna
    }
    return render(request,'vendedor/comunas.html', context)

@user_passes_test(es_vendedor)
def add_comuna_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio_envio = request.POST.get('precio_envio')

        nueva_comuna = Comuna(nombre=nombre, precio_envio=precio_envio)
        nueva_comuna.save()
      
    return redirect('Comunas')

@user_passes_test(es_vendedor)
def eliminar_comuna(request):
    if request.method == 'POST':
        comuna_id = request.POST.get('id_comuna')
        
        try:
            comuna = Comuna.objects.get(pk=comuna_id)
            comuna.delete()
            return JsonResponse({'success': True})
        except Comuna.DoesNotExist:
            return JsonResponse({'success': False})

@user_passes_test(es_vendedor)
def editar_comuna(request):
    if request.method == 'POST':
        comuna_id = request.POST.get('id_comuna')
        nombre = request.POST.get('nombre')
        precio_envio = request.POST.get('precio_envio')
        
        try:
            comuna = Comuna.objects.get(pk=comuna_id)
            comuna.nombre = nombre
            comuna.precio_envio = precio_envio
            comuna.save()
            return JsonResponse({'success': True})
        except Comuna.DoesNotExist:
            return JsonResponse({'success': False})

@user_passes_test(es_vendedor)
def cambiar_estado_arriendo(request):
    if request.method == 'POST':
        arriendo_id = request.POST.get('id_arriendo')
        estado = request.POST.get('estado')

        try:
            arriendo = Arriendo.objects.get(id=arriendo_id)
            arriendo.estado = estado
            arriendo.save()
            return JsonResponse({'success': True})
        except Arriendo.DoesNotExist:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})

@user_passes_test(es_vendedor)
def cambiar_estado_contacto(request):
    if request.method == 'POST':
        contacto_id = request.POST.get('id_contacto')
        estado = request.POST.get('estado')

        try:
            contacto = ContactMessage.objects.get(id=contacto_id)
            contacto.estado = estado
            contacto.save()
            return JsonResponse({'success': True})
        except ContactMessage.DoesNotExist:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})

@user_passes_test(es_vendedor)
def guardar_comentarios(request):
    if request.method == 'POST':
        id_contacto = request.POST.get('id_contacto')
        comentarios = request.POST.get('comentarios')
        
        try:
            contacto = ContactMessage.objects.get(id=id_contacto)
            contacto.comentarios = comentarios
            contacto.save()
            return JsonResponse({'success': True})
        except ContactMessage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'El contacto no existe.'})

    return JsonResponse({'success': False, 'error': 'Solicitud incorrecta.'})

@user_passes_test(es_vendedor)
def perfilvendedor(request):
    user = request.user
    perfil, created = PerfilVendedor.objects.get_or_create(user=user)
    perfil_form = PerfilVendedorForm(instance=perfil)

    if request.method == 'POST':
        perfil_form = PerfilVendedorForm(request.POST, request.FILES, instance=perfil) 
        if perfil_form.is_valid():
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            nombre_completo = f"{user.first_name} {user.last_name}"
            perfil.nombre_completo = nombre_completo
            perfil.correo = user.email
            perfil.imagen = request.FILES.get('perfilimg1')
            perfil.save()

    return render(request, 'vendedor/perfil.html', {'user': user, 'form': perfil_form})

@user_passes_test(es_vendedor)
def pedidos_clientes(request):
    arriendos = Arriendos.objects.all()
    if request.GET.get('pdf'):
        for arriendo in arriendos:
            pdf_response = generar_pdf(arriendo)
            if pdf_response.status_code != 200:
                return pdf_response

        return HttpResponse('PDFs generados exitosamente', status=200)
    return render(request, 'vendedor/pedidosCliente.html', {'arriendos': arriendos})

@user_passes_test(es_vendedor)
def pedidos_clientes_pendientes(request):
    arriendos = Arriendos.objects.filter(estado='Pendiente')
    if request.GET.get('pdf'):
        for arriendo in arriendos:
            pdf_response = generar_pdf(arriendo)
            if pdf_response.status_code != 200:
                return pdf_response

        return HttpResponse('PDFs generados exitosamente', status=200)
    return render(request, 'vendedor/pedidosClientePendiente.html', {'arriendos': arriendos})

@user_passes_test(es_vendedor)
def pedidos_clientes_realizados(request):
    arriendos = Arriendos.objects.filter(estado='Realizado')
    if request.GET.get('pdf'):
        for arriendo in arriendos:
            pdf_response = generar_pdf(arriendo)
            if pdf_response.status_code != 200:
                return pdf_response

        return HttpResponse('PDFs generados exitosamente', status=200)
    return render(request, 'vendedor/pedidosClienteRealizado.html', {'arriendos': arriendos})

@user_passes_test(es_vendedor)
def pedidos_clientes_cancelados(request):
    arriendos = Arriendos.objects.filter(estado='Cancelado')
    if request.GET.get('pdf'):
        for arriendo in arriendos:
            pdf_response = generar_pdf(arriendo)
            if pdf_response.status_code != 200:
                return pdf_response

        return HttpResponse('PDFs generados exitosamente', status=200)
    return render(request, 'vendedor/pedidosClienteCancelado.html', {'arriendos': arriendos})

@user_passes_test(es_vendedor)
def generar_pdf(request, arriendo_id):
    arriendo = get_object_or_404(Arriendo, id=arriendo_id)

    template_path = 'cliente/ticket.html'
    context = {'arriendo': arriendo}
    
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="arriendo_{arriendo.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

@user_passes_test(es_vendedor)
def cambiar_estado_arriendo_clientes(request):
    if request.method == 'POST':
        arriendo_id = request.POST.get('id_arriendo')
        nuevo_estado = request.POST.get('estado')
        
        try:
            arriendo = Arriendos.objects.get(id=arriendo_id)
            arriendo.estado = nuevo_estado
            arriendo.save()
            return JsonResponse({'success': True})
        except Arriendos.DoesNotExist:
            return JsonResponse({'success': False})
    
    return JsonResponse({'success': False})

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='vendedor').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        registros_por_mes = Arriendos.objects.annotate(month=TruncMonth('fecha')) \
            .values('month') \
            .annotate(count=Count('id')) \
            .order_by('month')

        labels = [registro['month'].strftime('%Y-%m') for registro in registros_por_mes]
        data = [registro['count'] for registro in registros_por_mes]

        context['labels'] = labels
        context['data'] = data

        return context

class GraficoTortaView(TemplateView):
    template_name = 'dashboard/grafico.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='vendedor').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        arriendos_por_cliente = Arriendos.objects.values('nombre_cliente') \
            .annotate(cantidad=Count('id')) \
            .order_by('-cantidad')  

        context['arriendos_por_cliente'] = arriendos_por_cliente

        return context

@user_passes_test(es_vendedor)
def mas_arrendada(request):
    herramientas_mas_arrendadas = Arriendos.objects.values('nombre_herramienta') \
        .annotate(total=Count('id')) \
        .order_by('-total')[:10]  # Puedes ajustar el número de herramientas que deseas mostrar

    return render(request, 'dashboard/masarrendada.html', {'herramientas_mas_arrendadas': herramientas_mas_arrendadas})

@user_passes_test(es_vendedor)
def arriendos_por_cliente(request):
    arriendos_por_cliente = Arriendo.objects.values('cliente') \
        .annotate(cantidad=Count('id')) \
        .order_by('-cantidad')[:10] 

    return render(request, 'dashboard/clientefrecuente.html', {'arriendos_por_cliente': arriendos_por_cliente})

@user_passes_test(es_vendedor)
def herramienta_mas_arrendada(request):
    herramientas_mas_arrendadas = Arriendo.objects.values('nombre_herramienta') \
        .annotate(total=Count('id')) \
        .order_by('-total')[:10]  

    return render(request, 'dashboard/herramientaArrendada.html', {'herramientas_mas_arrendadas': herramientas_mas_arrendadas})

@user_passes_test(es_vendedor)
def registros_por_fecha(request):
    registros_por_fecha = Arriendo.objects.values('fecha__month', 'fecha__year') \
        .annotate(total=Count('id')) \
        .order_by('fecha__year', 'fecha__month')

    return render(request, 'dashboard/registrosfecha.html', {'registros_por_fecha': registros_por_fecha})

@user_passes_test(es_vendedor)
def arriendos_por_comuna(request):
    arriendos_por_comuna = Arriendo.objects.values('comuna') \
        .annotate(total=Count('id')) \
        .order_by('-total')

    return render(request, 'dashboard/arriendoscomuna.html', {'arriendos_por_comuna': arriendos_por_comuna})

@user_passes_test(es_vendedor)
def arriendos_comuna(request):
    arriendoscomuna = Arriendos.objects.values('comuna') \
        .annotate(total=Count('id')) \
        .order_by('-total')

    return render(request, 'dashboard/arriendosporcomuna.html', {'arriendoscomuna': arriendoscomuna})


















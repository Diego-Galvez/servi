from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns = [

    #home
    path('', views.home_view, name='Home'),
    path('inicio/', views.inicio_view, name='Inicio'),
    path('contact/', views.contact, name='contact'),
    path('quienessomos/', views.quienes_view, name='QuienesSomos'),
    path('catalogo/', views.catalogo, name='Catalogo'),
    path('sesion/', views.sesion_view, name='Sesion'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('login/', views.login, name='login'),



    #Cliente
    path('cliente/', views.cliente_profile_view, name='cliente_profile'),
    path('servi/informacion/',views.informa, name='informa'), 
    path('add_arriendos/arriendo/', views.AddArriendos.as_view(), name='AddArriendos'),
    path('informacion/',views.informacion, name='informacion'),
    path('registro/cliente/', views.registrar_cliente, name='registro_cliente'),
    path('add_arriendos/', views.add_arriendos, name='add_arriendos'),
    path('perfil/cliente/', views.perfilcliente, name='perfilcliente'),
    path('lista_arriendos/', views.lista_arriendos, name='lista_arriendos'),
    path('lista_arriendos_pendientes/', views.arriendos_pendientes, name='ArriendoPendiente'),
    path('lista_arriendos_realizados/', views.arriendos_realizados, name='ArriendoRealizado'),
    path('lista_arriendos_cancelados/', views.arriendos_cancelados, name='ArriendoCancelado'),
    path('cancelar_pedido/', views.cancelar_pedido, name='cancelar_pedido'),
    path('actualizar_pedido/', views.actualizar_pedido, name='actualizar_pedido'),
    path('descargar_pdf/<int:arriendo_id>/', views.descargar_pdf, name='descargar_pdf'),
    path('catalogo/cliente', views.catalogocliente, name='CatalogoCliente'),
    





    #Vendedor
    path('ventas/', views.ventas_view, name='Ventas'),
    path('clientes/', views.clientes_view, name='Clientes'),
    path('add_cliente/', views.add_cliente_view, name='AddCliente'),
    path('edit_cliente/', views.edit_cliente_view, name='EditCliente'),   
    path('delete_cliente/', views.delete_cliente_view, name='DeleteCliente'),  
    path('productos/', views.productos_view, name='Productos'),
    path('add_producto/', views.add_producto_view, name='AddProducto'),
    path('edit_producto/', views.edit_producto_view, name='EditProduct'),
    path('delete_producto/', views.delete_producto_view, name='DeleteProduct'),  
    path('add_venta/',views.add_ventas.as_view(), name='AddVenta'),
    path('export/', views.export_pdf_view, name="ExportPDF" ),
    path('export/<id>/<iva>', views.export_pdf_view, name="ExportPDF" ),
    path('add_venta/',views.realizar_arriendo, name='AddVenta'),
    path('pedidos/',views.pedidos, name='pedidos'),
    path('pedidos/vendedor/pendientes',views.pedidos_vendedor_pendiente, name='pedidosVendedorPendiente'),
    path('pedidos/vendedor/realizados',views.pedidos_vendedor_realizado, name='pedidosVendedorRealizado'),
    path('pedidos/vendedor/cancelados',views.pedidos_vendedor_cancelado, name='pedidosVendedorCancelado'),
    path('mostrar_contactos/', views.mostrar_contactos, name='mostrar_contactos'),
    path('eliminar_arriendo/', views.eliminar_arriendo, name='eliminar_arriendo'),
    path('comunas_lista/', views.comunas_view, name='Comunas'),
    path('add_comuna/', views.add_comuna_view, name='AddComuna'),
    path('eliminar_comuna/', views.eliminar_comuna, name='eliminar_comuna'),
    path('editar_comuna/', views.editar_comuna, name='editar_comuna'),  
    path('arriendos/', views.arriendos_view, name='arriendos_view'),
    path('herramientas/', views.ListaProductosView.as_view(), name='Herramientas'),
    path('vendedor/', views.vendedor_profile_view, name='vendedor_profile'),
    path('cambiar_estado_arriendo/', views.cambiar_estado_arriendo, name='cambiar_estado_arriendo'),
    path('cambiar_estado_contacto/', views.cambiar_estado_contacto, name='cambiar_estado_contacto'),
    path('guardar_comentarios/', views.guardar_comentarios, name='guardar_comentarios'),
    path('perfil/vendedor/', views.perfilvendedor, name='perfilvendedor'),
    path('pedidos/clientes',views.pedidos_clientes, name='pedidosClientes'),
    path('pedidos/clientes/pendientes',views.pedidos_clientes_pendientes, name='pedidosClientesPendientes'),
    path('pedidos/clientes/cancelados',views.pedidos_clientes_cancelados, name='pedidosClientesCancelados'),
    path('pedidos/clientes/realizados',views.pedidos_clientes_realizados, name='pedidosClientesRealizados'),
    path('cambiar_estado_arriendo_clientes/', views.cambiar_estado_arriendo_clientes, name='cambiar_estado_arriendo_clientes'),
    path('generar_pdf/<int:arriendo_id>/', views.generar_pdf, name='generar_pdf'),
    path('generar_pdf_vendedor/<int:arriendo_id>/', views.generar_pdf_vendedor, name='generar_pdf_vendedor'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('grafico_torta/', views.GraficoTortaView.as_view(), name='grafico_torta'),
    path('masarrendada/', views.mas_arrendada, name='mas_arrendada'),
    path('arriendos_por_cliente/', views.arriendos_por_cliente, name='arriendos_por_cliente'),
    path('herramienta_mas_arrendada/', views.herramienta_mas_arrendada, name='herramienta_mas_arrendada'),
    path('registros_por_fecha/', views.registros_por_fecha, name='registros_por_fecha'),
    path('arriendos_por_comuna/', views.arriendos_por_comuna, name='arriendos_por_comuna'),
    path('arriendoscomuna/', views.arriendos_comuna, name='arriendoscomuna'),











    #recuperar contraseña
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),name='reset_password'),
    path('accounts/password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'),name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/pform.html'), name='password_reset_confirm'),
    path('accounts/reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_dones.html'),name='password_reset_complete'),



]
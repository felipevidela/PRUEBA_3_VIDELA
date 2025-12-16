from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.productos, name='productos'),
    path('categorias/', views.categorias, name='categorias'),
    path('categorias/<int:id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('pedir/', views.pedir, name= 'pedir'),
    path('seguimiento/<uuid:token>/', views.seguimiento, name='seguimiento'),
    path('productos/<int:id>/', views.producto_detalle, name="producto_detalle"),
    path("pedido/exito/", views.pedido_exito, name="pedido_exito"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

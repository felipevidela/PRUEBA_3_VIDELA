from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.productos, name='productos'),
    path('categorias/', views.categorias, name='categorias'),
    path('categorias/<int:id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('pedir/', views.pedir, name= 'pedir'),
    path('seguimiento/<uuid:token>/', views.seguimiento, name='seguimiento'),
]
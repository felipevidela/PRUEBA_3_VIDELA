from django.contrib import admin
from .models import Categoria, Producto, Pedido, Insumo 

# Register your models here.
from .models import Categoria, Producto, Pedido 

admin.site.register(Categoria)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    pass 

#Aquí use IA para aprender a como hacer visible el token en el admin
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    readonly_fields = ('token',)
    list_display = ('nombre_cliente', 'correo', 'estado', 'fecha_solicitada', 'token')

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'cantidad_disponible', 'unidad', 'marca', 'color')
    search_fields = ('nombre', 'marca', 'color')
    list_filter = ('tipo', 'marca', 'color')
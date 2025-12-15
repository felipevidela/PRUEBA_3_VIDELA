from django.contrib import admin

# Register your models here.
from .models import Categoria, Producto, Pedido 

admin.site.register(Categoria)
admin.site.register(Producto)

#Aquí use IA para aprender a como hacer visible el token en el admin
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    readonly_fields = ('token',)
    list_display = ('nombre_cliente', 'correo', 'estado', 'fecha_solicitada', 'token')
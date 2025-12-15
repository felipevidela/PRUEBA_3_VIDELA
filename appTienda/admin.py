from django.contrib import admin
from django.utils.html import format_html 
from .models import Pedido, PedidoImagen, Categoria, Producto, Insumo 

#Para hacer la clase PedidoImagenInline usé IA
class PedidoImagenInline(admin.TabularInline):
    model = PedidoImagen
    extra = 1
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="80" />', obj.imagen.url)
        return "-"
    preview.short_description = "Vista"

#Aquí use IA para aprender a como hacer visible el token en el admin
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    readonly_fields = ('token',)
    list_display = ('nombre_cliente', 'correo', 'estado', 'estado_pago', 'plataforma', 'fecha_solicitada', 'token')
    list_filter = ('estado', 'estado_pago', 'plataforma')
    search_fields = ('nombre_cliente', 'correo', 'token')
    inlines = [PedidoImagenInline]

admin.site.register(Categoria)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_base')
    list_filter = ('categoria',)
    search_fields = ('nombre',)

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'cantidad_disponible', 'unidad', 'marca', 'color')
    search_fields = ('nombre', 'marca', 'color')
    list_filter = ('tipo', 'marca', 'color')

#Esto me sugirió la IA para que respete la regla siempre la app
def save_model(self, request, obj, form, change):
    obj.full_clean() #Esto hace forzar las validaciones limpias clean()
    super().save_model(request, obj, form, change)
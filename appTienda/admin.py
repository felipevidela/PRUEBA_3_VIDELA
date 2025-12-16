from django import forms
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

    #Forzar validaciones del modelo (clean) al guardar desde el admin
    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    #Se crean checkboxes para poder eliminar una o varias imagenes por completo, ya que vi que era necesario tenerlas
    class ProductoAdminForm(forms.ModelForm):
        eliminar_imagen1 = forms.BooleanField(required=False, label="Eliminar imagen 1")
        eliminar_imagen2 = forms.BooleanField(required=False, label="Eliminar imagen 2")
        eliminar_imagen3 = forms.BooleanField(required=False, label="Eliminar imagen 3")

        class Meta:
            model = Producto
            fields = "__all__"

        def save(self, commit=True):
            producto = super().save(commit=False)

            for imagen_field, flag_field in [
                ("imagen1", "eliminar_imagen1"),
                ("imagen2", "eliminar_imagen2"),
                ("imagen3", "eliminar_imagen3"),
            ]:
                if self.cleaned_data.get(flag_field):
                    imagen = getattr(producto, imagen_field)
                    if imagen:
                        imagen.delete(save=False)
                    setattr(producto, imagen_field, None)

            if commit:
                producto.save()
                self.save_m2m()

            return producto

    form = ProductoAdminForm
    list_display = ('preview_imagen', 'nombre', 'categoria', 'precio_base', 'destacado')
    list_filter = ('categoria', 'destacado')
    search_fields = ('nombre',)
    readonly_fields = ('preview_imagen',)
    list_editable = ('destacado',)
    list_display_links = ('nombre',)

    def preview_imagen(self, obj):
        if obj.imagen1:
            return format_html(
                '<img src="{}" width="80" style="border-radius:4px;" />',
                obj.imagen1.url
            )
        return "-"
    
    preview_imagen.short_description = "Imagen"

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'cantidad_disponible', 'unidad', 'marca', 'color')
    search_fields = ('nombre', 'marca', 'color')
    list_filter = ('tipo', 'marca', 'color')

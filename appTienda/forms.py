from django import forms
from .models import Pedido 

class PedidoForm(forms.ModelForm):
    class Meta: 
        model = Pedido 
        fields = ['nombre_cliente', 'correo', 'descripcion', 'fecha_solicitada']
        widgets = {
            'fecha_solicitada': forms.DateInput(attrs={'type':'date'})
        }


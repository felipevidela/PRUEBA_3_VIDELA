from django import forms
from .models import Pedido 

class PedidoForm(forms.ModelForm):
    class Meta: 
        model = Pedido 
        fields = ['producto', 'nombre_cliente','correo','descripcion','fecha_solicitada']
        widgets = {
            'producto': forms.HiddenInput(),
            'fecha_solicitada': forms.DateInput(attrs={'type': 'date'})
        }


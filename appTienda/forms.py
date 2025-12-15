from django import forms 

class PedidoForm(forms.Form):
    nombre_cliente = forms.CharField()
    correo = forms.EmailField()
    descripcion = forms.CharField(widget=forms.Textarea)
    fecha_solicitada = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
from django import forms
from .models import Pedido


class MultiClearableFileInput(forms.ClearableFileInput):
    #Esto es para que permita que suba multiples archivos
    allow_multiple_selected = True


class MultiFileField(forms.FileField):
    """
    A FileField that accepts multiple uploaded files and returns them as a list.
    This avoids the default validation error when the widget sends a list.
    """

    def clean(self, data, initial=None):
        if not data:
            return []

        archivos = data if isinstance(data, (list, tuple)) else [data]
        limpiados = []

        for archivo in archivos:
            if not archivo:
                continue
            limpiados.append(super().clean(archivo, initial))

        return limpiados


class PedidoForm(forms.ModelForm):
 #Permite subir multiples imagenes 
    imagenes = MultiFileField(
        required=False,
        widget=MultiClearableFileInput(attrs={"multiple": True})
    )

    class Meta:
        model = Pedido
        fields = ["producto", "nombre_cliente", "correo", "descripcion", "fecha_solicitada"]
        widgets = {
            "producto": forms.HiddenInput(),
            "fecha_solicitada": forms.DateInput(attrs={"type": "date"}),
        }

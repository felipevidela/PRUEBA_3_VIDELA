from django import forms
from .models import Pedido


class MultiClearableFileInput(forms.ClearableFileInput):
    #Esto es para que permita que suba multiples archivos
    allow_multiple_selected = True

#Esto permite que el campi acepte varias cargas y las valide una por una 
class MultiFileField(forms.FileField):

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
#Esto es para obligar al usuario a ingresar por lo menos uno de estos 3 datos 
    def clean(self):
        cleaned = super().clean()
        contacto = [
            cleaned.get("correo"),
            cleaned.get("telefono"),
            cleaned.get("usuario_red_social"),
        ]
        if not any(contacto):
            raise forms.ValidationError(
                "Debes ingresar al menos un dato de contacto: correo, teléfono o usuario de red social."
            )
        return cleaned
#Esto vincula al formulario con el Pedido y se usa los widgets para personalizar el Pedido
    class Meta:
        model = Pedido
        fields = ["producto", "nombre_cliente", "telefono", "correo", "usuario_red_social", "descripcion", "fecha_solicitada"]
        widgets = {
            "producto": forms.HiddenInput(),
            "fecha_solicitada": forms.DateInput(attrs={"type": "date"}),
        }

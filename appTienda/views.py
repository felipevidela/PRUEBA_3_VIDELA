from django.shortcuts import render
from .models import Producto 


# Create your views here.
def home(request):
    return render(request, 'index.html')


def productos(request):
    lista = Producto.objects.all()
    data = {
        'productos': lista
    }
    return render(request, 'productos.html', data)

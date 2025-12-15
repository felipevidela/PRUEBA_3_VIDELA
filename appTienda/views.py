from django.shortcuts import render
from .models import Producto, Categoria, Pedido 
from .forms import PedidoForm 


# Create your views here.
def home(request):
    return render(request, 'index.html')


def productos(request):
    lista = Producto.objects.all()
    data = {
        'productos': lista
    }
    return render(request, 'productos.html', data)

def categorias(request):
    lista = Categoria.objects.all()
    data = {
        'categorias': lista
    }
    return render(request, 'categorias.html', data)

def productos_por_categoria(request, id):
    cat = Categoria.objects.get(id=id)
    lista = Producto.objects.filter(categoria=cat)
    data = {
        'categoria': cat, 
        'productos': lista
    }
    return render(request, 'productos_categoria.html',data)

def pedir(request):
    data = {
        'form': PedidoForm()
    }

    if request.method == 'POST': 
        formulario = PedidoForm(request.POST)
        if formulario.is_valid(): 
            pedido = formulario.save()
            data['mensaje'] = 'Pedido enviado exitosamente'
            data['token'] = pedido.token #Esto es para obtener el objeto y su token, servirá para que en el mensaje tenga un link de seguimiento 
            data['form'] = PedidoForm() #Esto es para limpiar el formulario
        else: 
            data['form'] = formulario 
    
    return render(request, 'pedido_form.html', data)

def seguimiento(request, token): 
    pedido = Pedido.objects.get(token=token)
    data = {
        'pedido': pedido 
    }
    return render(request, 'seguimiento.html', data)
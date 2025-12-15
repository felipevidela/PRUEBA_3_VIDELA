from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria, Pedido
from .forms import PedidoForm

# Create your views here.

def home(request):
    return render(request, "index.html")

# Catálogo público con filtros

def productos(request):
    productos_qs = Producto.objects.all()
    categorias_qs = Categoria.objects.all()

    categoria_id = request.GET.get("categoria")
    q = request.GET.get("q")
    solo_destacados = request.GET.get("solo_destacados")

    if categoria_id:
        productos_qs = productos_qs.filter(categoria_id=categoria_id)

    if q:
        productos_qs = productos_qs.filter(nombre__icontains=q)

    # Si viene ?solo_destacados=1, filtra solo destacados
    if solo_destacados == "1":
        productos_qs = productos_qs.filter(destacado=True)

    return render(request, "productos.html", {
        "productos": productos_qs,
        "categorias": categorias_qs,
        "categoria_id": categoria_id or "",
        "q": q or "",
        "solo_destacados": solo_destacados or "",
    })


def producto_detalle(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, "producto_detalle.html", {"producto": producto})


def categorias(request):
    lista = Categoria.objects.all()
    return render(request, "categorias.html", {"categorias": lista})


def productos_por_categoria(request, id):
    cat = get_object_or_404(Categoria, id=id)
    lista = Producto.objects.filter(categoria=cat)
    return render(request, "productos_categoria.html", {"categoria": cat, "productos": lista})


def pedir(request):
    data = {"form": PedidoForm()}

    if request.method == "POST":
        formulario = PedidoForm(request.POST)
        if formulario.is_valid():
            pedido = formulario.save()
            data["mensaje"] = "Pedido enviado exitosamente"
            # Mostrar el link de seguimiento
            data["token"] = pedido.token
            # Limpiar el formulario
            data["form"] = PedidoForm()
        else:
            data["form"] = formulario

    return render(request, "pedido_form.html", data)


def seguimiento(request, token):
    pedido = get_object_or_404(Pedido, token=token)
    return render(request, "seguimiento.html", {"pedido": pedido})
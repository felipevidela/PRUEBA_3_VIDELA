from django.shortcuts import render, get_object_or_404, redirect 
from .models import Producto, Categoria, Pedido, PedidoImagen 
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
    producto_id = request.GET.get("producto_id") or request.POST.get("producto")

    if request.method == "POST":
        formulario = PedidoForm(request.POST, request.FILES)
        if formulario.is_valid():
            pedido = formulario.save()

            for archivo in formulario.cleaned_data.get("imagenes", []):
                PedidoImagen.objects.create(pedido=pedido, imagen=archivo)

            return redirect("pedido_exito")

    else:
        formulario = PedidoForm(initial={"producto": producto_id}) if producto_id else PedidoForm()

    return render(request, "pedido_form.html", {"form": formulario})


def seguimiento(request, token):
    pedido = get_object_or_404(Pedido, token=token)
    return render(request, "seguimiento.html", {"pedido": pedido})

def pedido_exito(request):
    return render(request, "pedido_exito.html")

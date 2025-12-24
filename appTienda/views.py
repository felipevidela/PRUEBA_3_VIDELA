from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria, Pedido, PedidoImagen
from .forms import PedidoForm
#Con esto nos aseguramos de que la página de resumen de pedidos no sea pública
# y que se puede ver estando logeada en el admin de django
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Count
from django.db.models.functions import Upper

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
            pedido = formulario.save(commit=False)
            pedido.plataforma = "SITIO_WEB"
            pedido.save()

            for archivo in formulario.cleaned_data.get("imagenes", []):
                PedidoImagen.objects.create(pedido=pedido, imagen=archivo)
            
            url_seguimiento = request.build_absolute_uri(f"/seguimiento/{pedido.token}/")
            return render (request, "pedido_exito.html", {
                "token": pedido.token,
                "url_seguimiento": url_seguimiento,
            })
    else:
        formulario = PedidoForm(initial={"producto": producto_id}) if producto_id else PedidoForm()

    return render(request, "pedido_form.html", {"form": formulario})

def seguimiento(request, token):
    pedido = get_object_or_404(Pedido, token=token)
    return render(request, "seguimiento.html", {"pedido": pedido})

def pedido_exito(request):
    return render(request, "pedido_exito.html")

@login_required
def resumen_pedidos(request):
    if not request.user.is_staff: 
        return HttpResponseForbidden("Solo para usuarios autorizados.")
    
    por_estado = (
        Pedido.objects.values('estado')
        .annotate(total=Count('id'))
        .order_by('-total') #Esto es para ordena esos resultados de mayor a menor 
    )

    por_pago = (
        Pedido.objects.values('estado_pago')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    #Sirve para mostrar los 10 ultimos pedidos creados 
    recientes = Pedido.objects.select_related('producto').order_by('-id')[:10] 

    return render(request, "resumen_pedidos.html", {
        "por_estado" : por_estado,
        "por_pago": por_pago, 
        "recientes": recientes,
    })
@login_required
def reporte_pedidos(request):
    estado = request.GET.get('estado')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    ESTADOS = Pedido._meta.get_field('estado').choices

    pedidos = Pedido.objects.all()

    # Filtros
    if estado:
        pedidos = pedidos.filter(estado=estado)

    if desde:
        pedidos = pedidos.filter(fecha_solicitada__gte=desde)

    if hasta:
        pedidos = pedidos.filter(fecha_solicitada__lte=hasta)

    # Datos para gráfico (ANTES del order_by para que agrupe correctamente)
    resumen = (
        pedidos
        .values('estado')
        .annotate(total=Count('id'))
    )

    # Ordenar para la tabla (DESPUÉS del resumen)
    pedidos = pedidos.order_by('-fecha_solicitada')

    context = {
        'pedidos': pedidos,
        'resumen': resumen,
        'estado': estado,
        'desde': desde,
        'hasta': hasta,
        'estados': ESTADOS,
    }

    return render(request, 'reportes/pedidos.html', context)
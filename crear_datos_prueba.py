#!/usr/bin/env python
"""
Script para crear datos de prueba: 20 productos, 20 insumos y 20 pedidos
"""
import os
import sys
import django
import requests
from io import BytesIO
from datetime import date, timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PRUEBA_3_VIDELA.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.files.base import ContentFile
from appTienda.models import Categoria, Producto, Insumo, Pedido

def descargar_imagen(url, nombre):
    """Descarga una imagen desde una URL y retorna un ContentFile"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return ContentFile(response.content, name=nombre)
    except Exception as e:
        print(f"  Error descargando imagen: {e}")
    return None

def crear_categorias():
    """Crea las categorías de ropa"""
    print("\n=== Creando Categorías ===")
    categorias_nombres = ['Camisetas', 'Pantalones', 'Vestidos', 'Chaquetas', 'Faldas']
    categorias = {}

    for nombre in categorias_nombres:
        categoria, created = Categoria.objects.get_or_create(nombre=nombre)
        categorias[nombre] = categoria
        status = "creada" if created else "existente"
        print(f"  {nombre}: {status}")

    return categorias

def crear_productos(categorias):
    """Crea 20 productos de ropa con imágenes"""
    print("\n=== Creando Productos ===")

    # URLs de imágenes de ropa de Unsplash (gratuitas)
    imagenes_ropa = [
        "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",  # camiseta blanca
        "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=400",  # camiseta estampada
        "https://images.unsplash.com/photo-1625910513413-5fc45f8c50e2?w=400",  # polo
        "https://images.unsplash.com/photo-1564257631407-4deb1f99d992?w=400",  # blusa
        "https://images.unsplash.com/photo-1542272454315-4c01d7abdf4a?w=400",  # jeans
        "https://images.unsplash.com/photo-1517438476312-10d79c077509?w=400",  # cargo
        "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400",  # pantalon vestir
        "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400",  # shorts
        "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400",  # vestido casual
        "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=400",  # vestido noche
        "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400",  # vestido floral
        "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400",  # maxi vestido
        "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",  # chaqueta cuero
        "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=400",  # chaqueta deportiva
        "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400",  # blazer
        "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400",  # sudadera
        "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=400",  # falda midi
        "https://images.unsplash.com/photo-1577900232427-18219b9166a0?w=400",  # falda plisada
        "https://images.unsplash.com/photo-1582142839970-2b9e04b60f65?w=400",  # minifalda
        "https://images.unsplash.com/photo-1592301933927-35b597393c0a?w=400",  # falda larga
    ]

    productos_data = [
        ("Camiseta Básica Blanca", "Camisetas", 15000, "Camiseta de algodón 100% suave y cómoda, ideal para uso diario."),
        ("Camiseta Estampada Urbana", "Camisetas", 22000, "Camiseta con diseño urbano moderno, perfecta para un look casual."),
        ("Polo Deportivo", "Camisetas", 28000, "Polo deportivo con tejido transpirable, ideal para actividades al aire libre."),
        ("Blusa Elegante", "Camisetas", 35000, "Blusa de seda sintética con corte elegante para ocasiones especiales."),
        ("Pantalón Jeans Clásico", "Pantalones", 45000, "Jeans de corte recto clásico, denim de alta calidad."),
        ("Pantalón Cargo", "Pantalones", 42000, "Pantalón cargo con múltiples bolsillos, estilo militar moderno."),
        ("Pantalón de Vestir", "Pantalones", 55000, "Pantalón formal de tela premium, perfecto para oficina."),
        ("Shorts Deportivos", "Pantalones", 18000, "Shorts livianos y cómodos para ejercicio y uso casual."),
        ("Vestido Casual", "Vestidos", 38000, "Vestido casual de algodón, cómodo y versátil para el día a día."),
        ("Vestido de Noche", "Vestidos", 85000, "Vestido elegante de noche con detalles brillantes."),
        ("Vestido Floral", "Vestidos", 42000, "Vestido con estampado floral, perfecto para primavera."),
        ("Maxi Vestido Bohemio", "Vestidos", 58000, "Vestido largo estilo bohemio, fluido y elegante."),
        ("Chaqueta de Cuero", "Chaquetas", 95000, "Chaqueta de cuero sintético de alta calidad, estilo clásico."),
        ("Chaqueta Deportiva", "Chaquetas", 48000, "Chaqueta deportiva impermeable, ideal para actividades outdoor."),
        ("Blazer Formal", "Chaquetas", 72000, "Blazer formal de corte moderno, perfecto para reuniones de trabajo."),
        ("Sudadera con Capucha", "Chaquetas", 32000, "Sudadera cómoda con capucha, ideal para días frescos."),
        ("Falda Midi", "Faldas", 28000, "Falda midi elegante, largo hasta la rodilla."),
        ("Falda Plisada", "Faldas", 35000, "Falda plisada con movimiento fluido, estilo sofisticado."),
        ("Minifalda Denim", "Faldas", 25000, "Minifalda de jean con estilo juvenil y moderno."),
        ("Falda Larga Elegante", "Faldas", 45000, "Falda larga de tela fluida, perfecta para eventos formales."),
    ]

    for i, (nombre, cat_nombre, precio, descripcion) in enumerate(productos_data):
        # Verificar si ya existe
        if Producto.objects.filter(nombre=nombre).exists():
            print(f"  {i+1}. {nombre}: ya existe, saltando...")
            continue

        print(f"  {i+1}. Creando {nombre}...")

        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            categoria=categorias[cat_nombre],
            precio_base=precio,
            destacado=(i % 4 == 0)  # Cada 4to producto es destacado
        )

        # Descargar imagen
        imagen = descargar_imagen(imagenes_ropa[i], f"{nombre.lower().replace(' ', '_')}.jpg")
        if imagen:
            producto.imagen1 = imagen
            print(f"     Imagen descargada correctamente")

        producto.save()
        print(f"     Guardado con precio ${precio:,}")

    print(f"\nTotal productos en BD: {Producto.objects.count()}")

def crear_insumos():
    """Crea 20 insumos de ropa"""
    print("\n=== Creando Insumos ===")

    insumos_data = [
        ("Tela Algodón Premium", "tela", 150, "metros", "TextilPro", "Blanco"),
        ("Tela Algodón Estampada", "tela", 80, "metros", "Fantasía Textil", "Multicolor"),
        ("Tela Denim", "tela", 120, "metros", "JeansCo", "Azul"),
        ("Tela Seda", "tela", 45, "metros", "SilkWorld", "Negro"),
        ("Tela Lino", "tela", 90, "metros", "NaturalFabrics", "Beige"),
        ("Tela Poliéster", "tela", 200, "metros", "SyntheticPro", "Gris"),
        ("Cuero Sintético", "cuero", 60, "metros", "LeatherStyle", "Negro"),
        ("Cuero Natural", "cuero", 35, "metros", "Curtiembre Sur", "Marrón"),
        ("Cuero Grabado", "cuero", 25, "metros", "ArtLeather", "Café"),
        ("Botones Metálicos", "metal", 500, "unidades", "MetalButtons", "Plateado"),
        ("Cremalleras Metal", "metal", 300, "unidades", "ZipperPro", "Dorado"),
        ("Hebillas Cinturón", "metal", 150, "unidades", "BuckleCo", "Negro"),
        ("Remaches Decorativos", "metal", 800, "unidades", "RivetStyle", "Bronce"),
        ("Botones Plástico", "plastico", 1000, "unidades", "PlasticButtons", "Transparente"),
        ("Broches Plástico", "plastico", 600, "unidades", "ClipCo", "Blanco"),
        ("Elástico Ancho", "otro", 200, "metros", "ElasticPro", "Negro"),
        ("Hilo Poliéster", "otro", 100, "rollos", "ThreadMaster", "Varios"),
        ("Entretela", "otro", 180, "metros", "InterlineCo", "Blanco"),
        ("Forro Satinado", "tela", 95, "metros", "SatinWorld", "Rojo"),
        ("Encaje Decorativo", "tela", 50, "metros", "LaceArt", "Crema"),
    ]

    for i, (nombre, tipo, cantidad, unidad, marca, color) in enumerate(insumos_data):
        insumo, created = Insumo.objects.get_or_create(
            nombre=nombre,
            defaults={
                'tipo': tipo,
                'cantidad_disponible': cantidad,
                'unidad': unidad,
                'marca': marca,
                'color': color
            }
        )
        status = "creado" if created else "existente"
        print(f"  {i+1}. {nombre} ({tipo}): {status}")

    print(f"\nTotal insumos en BD: {Insumo.objects.count()}")

def crear_pedidos():
    """Crea 20 pedidos con todos los estados posibles"""
    print("\n=== Creando Pedidos ===")

    # Nombres chilenos ficticios
    clientes = [
        ("María González", "maria.gonzalez@email.cl", "912345678", "@maria_gon"),
        ("Juan Pérez", "juan.perez@email.cl", "923456789", "@juanp"),
        ("Carla Silva", "carla.silva@email.cl", "934567890", "@carlasilva"),
        ("Pedro Muñoz", "pedro.munoz@email.cl", "945678901", "@pedrom"),
        ("Ana Rodríguez", "ana.rodriguez@email.cl", "956789012", "@anarodri"),
        ("Diego Fernández", "diego.fernandez@email.cl", "967890123", "@diegof"),
        ("Valentina López", "valentina.lopez@email.cl", "978901234", "@valelop"),
        ("Sebastián Martínez", "sebastian.martinez@email.cl", "989012345", "@sebam"),
        ("Francisca Torres", "francisca.torres@email.cl", "990123456", "@frantorres"),
        ("Matías Vargas", "matias.vargas@email.cl", "901234567", "@matiasv"),
        ("Camila Soto", "camila.soto@email.cl", "912345670", "@camisoto"),
        ("Nicolás Ramírez", "nicolas.ramirez@email.cl", "923456780", "@nicoram"),
        ("Javiera Díaz", "javiera.diaz@email.cl", "934567801", "@javiediaz"),
        ("Felipe Rojas", "felipe.rojas@email.cl", "945678012", "@feliperoj"),
        ("Constanza Herrera", "constanza.herrera@email.cl", "956780123", "@consherr"),
        ("Tomás Fuentes", "tomas.fuentes@email.cl", "967801234", "@tomasfue"),
        ("Isidora Castillo", "isidora.castillo@email.cl", "978012345", "@isicast"),
        ("Benjamín Morales", "benjamin.morales@email.cl", "980123456", "@benjamor"),
        ("Antonia Reyes", "antonia.reyes@email.cl", "901234560", "@antoniar"),
        ("Lucas Espinoza", "lucas.espinoza@email.cl", "912340567", "@lucasesp"),
    ]

    # Distribución de pedidos según el plan
    pedidos_config = [
        ('SOLICITADO', 'PENDIENTE', 'FACEBOOK'),
        ('SOLICITADO', 'PENDIENTE', 'INSTAGRAM'),
        ('SOLICITADO', 'PARCIAL', 'WHATSAPP'),
        ('APROBADO', 'PENDIENTE', 'PRESENCIAL'),
        ('APROBADO', 'PARCIAL', 'SITIO_WEB'),
        ('APROBADO', 'PAGADO', 'OTRA'),
        ('EN_PROCESO', 'PENDIENTE', 'FACEBOOK'),
        ('EN_PROCESO', 'PARCIAL', 'INSTAGRAM'),
        ('EN_PROCESO', 'PAGADO', 'WHATSAPP'),
        ('REALIZADA', 'PENDIENTE', 'PRESENCIAL'),
        ('REALIZADA', 'PARCIAL', 'SITIO_WEB'),
        ('REALIZADA', 'PAGADO', 'OTRA'),
        ('ENTREGADA', 'PENDIENTE', 'FACEBOOK'),
        ('ENTREGADA', 'PARCIAL', 'INSTAGRAM'),
        ('ENTREGADA', 'PAGADO', 'WHATSAPP'),
        ('FINALIZADA', 'PAGADO', 'PRESENCIAL'),
        ('FINALIZADA', 'PAGADO', 'SITIO_WEB'),
        ('FINALIZADA', 'PAGADO', 'OTRA'),
        ('CANCELADA', 'PENDIENTE', 'FACEBOOK'),
        ('CANCELADA', 'PARCIAL', 'INSTAGRAM'),
    ]

    descripciones_pedidos = [
        "Camiseta personalizada con logo empresarial",
        "Vestido para evento de graduación",
        "Conjunto deportivo completo",
        "Chaqueta con bordado personalizado",
        "Pantalones a medida para uniforme",
        "Falda plisada para colegio",
        "Blusa de seda para matrimonio",
        "Sudadera con estampado personalizado",
        "Vestido de novia modificado",
        "Traje formal completo",
        "Ropa deportiva para equipo de fútbol",
        "Uniformes escolares (5 unidades)",
        "Vestido de fiesta con ajustes",
        "Chaqueta de cuero personalizada",
        "Conjunto casual para sesión de fotos",
        "Ropa de trabajo con logo bordado",
        "Vestido de dama de honor",
        "Abrigo de invierno a medida",
        "Poleras para evento corporativo",
        "Conjunto elegante para entrevista",
    ]

    productos = list(Producto.objects.all())

    for i, (estado, estado_pago, plataforma) in enumerate(pedidos_config):
        cliente = clientes[i]
        nombre_cliente, correo, telefono, usuario_red = cliente

        # Verificar si ya existe un pedido similar
        if Pedido.objects.filter(nombre_cliente=nombre_cliente, descripcion=descripciones_pedidos[i]).exists():
            print(f"  {i+1}. Pedido de {nombre_cliente}: ya existe, saltando...")
            continue

        # Fecha solicitada aleatoria en los próximos 30 días
        fecha_solicitada = date.today() + timedelta(days=random.randint(1, 30))

        pedido = Pedido(
            nombre_cliente=nombre_cliente,
            telefono=telefono,
            usuario_red_social=usuario_red,
            correo=correo,
            descripcion=descripciones_pedidos[i],
            fecha_solicitada=fecha_solicitada,
            estado=estado,
            estado_pago=estado_pago,
            plataforma=plataforma,
        )

        # Asignar plataforma_otra si corresponde
        if plataforma == 'OTRA':
            pedido.plataforma_otra = "TikTok"

        # Asignar producto si hay disponibles
        if productos:
            pedido.producto = random.choice(productos)

        pedido.save()
        print(f"  {i+1}. {nombre_cliente}: {estado} | {estado_pago} | {plataforma}")

    print(f"\nTotal pedidos en BD: {Pedido.objects.count()}")

    # Resumen de estados
    print("\n=== Resumen de Estados ===")
    for estado, _ in Pedido.ESTADOS:
        count = Pedido.objects.filter(estado=estado).count()
        print(f"  {estado}: {count}")

def main():
    print("=" * 50)
    print("SCRIPT DE CREACIÓN DE DATOS DE PRUEBA")
    print("=" * 50)

    # Crear categorías primero
    categorias = crear_categorias()

    # Crear productos
    crear_productos(categorias)

    # Crear insumos
    crear_insumos()

    # Crear pedidos
    crear_pedidos()

    print("\n" + "=" * 50)
    print("PROCESO COMPLETADO")
    print("=" * 50)

if __name__ == '__main__':
    main()

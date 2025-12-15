import uuid 
# Usé uuid por que es lo que encontré en internet que puede servirme para tener un token único de seguimiento para cada pedido"
from django.db import models


class Categoria(models.Model): 
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre 

class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio_base = models.IntegerField()

    imagen1 = models.ImageField(upload_to = 'productos/', null=True, blank=True)
    imagen2 = models.ImageField(upload_to='productos/', null=True, blank=True)
    imagen3 = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model): 
    nombre_cliente = models.CharField(max_length=100)
    correo = models.EmailField()
    descripcion = models.TextField()
    fecha_solicitada = models.DateField()

    estado = models.CharField(
        max_length=20,
        choices= [
            ('solicitado', 'Solicitado'),
            ('en_proceso', 'En proceso'),
            ('finalizado', 'Finalizado'),
        ],
        default='solicitado'
    )

    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    #Aquí me apoye de la IA para hacer esto por que no sabía como implementarlo.

    def __str__(self):
        return self.nombre_cliente

class Insumo(models.Model): 
    TIPO_CHOICES = [
        ('tela', 'Tela'),
        ('cuero', 'Cuero'),
        ('plastico', 'Plástico'),
        ('metal', 'Metal'),
        ('otro', "Otro"),
        ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad_disponible = models.IntegerField()
    unidad = models.CharField(max_length=20, null=True, blank=True)
    marca = models.CharField(max_length=50)
    color = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre
   

import uuid
# Usé uuid porque sirve para tener un token único de seguimiento para cada pedido.

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import date 


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    #Esto es para ordenar Categoria 
    class Meta: 
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre



class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio_base = models.PositiveIntegerField()
    destacado = models.BooleanField(default=False)
    #Esto es para ordenar Producto
    class Meta: 
        ordering = ['nombre']


    imagen1 = models.ImageField(upload_to='productos/', null=True, blank=True)
    imagen2 = models.ImageField(upload_to='productos/', null=True, blank=True)
    imagen3 = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    ESTADOS = [
        ('SOLICITADO', 'Solicitado'),
        ('APROBADO', 'Aprobado'),
        ('EN_PROCESO', 'En proceso'),
        ('REALIZADA', 'Realizada'),
        ('ENTREGADA', 'Entregada'),
        ('FINALIZADA', 'Finalizada'),
        ('CANCELADA', 'Cancelada'),
    ]

    PAGOS = [
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL', 'Parcial'),
        ('PAGADO', 'Pagado'),
    ]

    PLATAFORMAS = [
        ('FACEBOOK', 'Facebook'),
        ('INSTAGRAM', 'Instagram'),
        ('WHATSAPP', 'WhatsApp'),
        ('PRESENCIAL', 'Presencial'),
        ('SITIO_WEB', 'Sitio Web'),
        ('OTRA', 'Otra'),
    ]

    nombre_cliente = models.CharField(max_length=100)
    #Aqui se crea un validor de 9 digitos para el telefono
    telefono = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r"^\d{9}$",
                message="El teléfono debe tener exactamente 9 dígitos.",
            )
        ], 
        blank=True, null=True 
    )
    usuario_red_social = models.CharField(max_length=100, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    descripcion = models.TextField()
    fecha_solicitada = models.DateField(blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=True, blank=True)

    estado = models.CharField(max_length=20, choices=ESTADOS, default='SOLICITADO')
    estado_pago = models.CharField(max_length=20, choices=PAGOS, default='PENDIENTE')

    plataforma = models.CharField(max_length=20, choices=PLATAFORMAS, default='WHATSAPP')
    plataforma_otra = models.CharField(max_length=50, blank=True, null=True)

    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    #Esto es para ordenar Pedido
    class Meta: 
        ordering = ['nombre_cliente']

    def clean(self):
        # Regla: no se puede finalizar si no está pagado
        if self.estado == 'FINALIZADA' and self.estado_pago != 'PAGADO':
            raise ValidationError(
                "No se puede marcar como Finalizada si el estado de pago no es Pagado."
            )

        # Regla: si la plataforma es 'Otra' debe especificarse
        if self.plataforma == 'OTRA' and not self.plataforma_otra:
            raise ValidationError("Si la plataforma es 'Otra', debes especificarla.")

        # Si no es 'Otra', limpiar el texto
        if self.plataforma != 'OTRA':
            self.plataforma_otra = None
        # Validar que la fecha solicitada no sea anterior a hoy
        if self.fecha_solicitada and self.fecha_solicitada < date.today():
            raise ValidationError(
                "La fecha solicitada no puede ser anterior a la fecha de hoy."
            )

    def __str__(self):
        return f"{self.nombre_cliente} - {self.get_estado_display()}"


class PedidoImagen(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="pedidos/")
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Imagen de {self.pedido.nombre_cliente}"


class Insumo(models.Model):
    TIPO_CHOICES = [
        ('tela', 'Tela'),
        ('cuero', 'Cuero'),
        ('plastico', 'Plástico'),
        ('metal', 'Metal'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad_disponible = models.PositiveIntegerField()
    unidad = models.CharField(max_length=20, null=True, blank=True)
    marca = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    #Esto es para ordenar Insumo 
    class Meta: 
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

from django.db import models

# Create your models here.

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
    

from django.db import models

class Insumo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    stock = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.CharField(max_length=50)
    #stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    insumos = models.ManyToManyField(Insumo, blank=True, related_name='productos')

    def __str__(self):
        return self.nombre
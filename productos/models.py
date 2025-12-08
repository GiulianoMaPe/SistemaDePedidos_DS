from django.db import models

class Insumo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    stock = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    es_extra = models.BooleanField(default=False, verbose_name="¿Es extra?")

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    insumos = models.ManyToManyField(Insumo, blank=True, related_name='productos')

    def __str__(self):
        return self.nombre

    def tiene_stock_suficiente(self):
        for insumo in self.insumos.all():
            if insumo.stock <= 0:
                return False  # Encontró un ingrediente agotado
        return True
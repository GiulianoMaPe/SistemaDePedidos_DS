from django.db import models
from productos.models import Producto
from django.contrib.auth.models import User  # <--- IMPORTAR ESTO

class Pedido(models.Model):
    ESTADOS = [
        ('En preparación', 'En preparación'),
        ('Listo para entregar', 'Listo para entregar'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    ]

    METODOS_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
    ]

    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='En preparación')
    cliente = models.CharField(max_length=100)
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO, default='Efectivo')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    personalizacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido {self.pedido.id})"
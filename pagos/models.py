from django.db import models

# Create your models here.
class Pago(models.Model):
    numero_operacion = models.CharField(max_length=20, unique=True)
    estado = models.CharField(max_length=20)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    comprador_email = models.EmailField()
    fecha_pago = models.DateTimeField()
    metodo_pago = models.CharField(max_length=50)
    tarjeta_ultimos_digitos = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return f"Pago {self.numero_operacion} - {self.estado}"

class ValidacionPago(models.Model):
    estudiante = models.OneToOneField('Estudiante', on_delete=models.CASCADE)
    pago = models.OneToOneField('Pago', on_delete=models.CASCADE)
    fecha_validacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante} - {self.pago.numero_operacion}" 
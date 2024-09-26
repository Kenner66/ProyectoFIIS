from django.db import models

# Create your models here.
from django.db import models
from usuarios.models import Usuario  # Importa el modelo Usuario

class Estudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10)
    base = models.CharField(max_length=20, unique=True)  
    carrera = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.usuario.username} - {self.base}"

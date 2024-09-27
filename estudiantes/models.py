from django.db import models

# Create your models here.
from django.db import models
from usuarios.models import Usuario  # Importa el modelo Usuario

class Estudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10,unique=True)
    base = models.CharField(max_length=20)  
    carrera = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.usuario.username} - {self.base}"

class InformacionPersonal(models.Model):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE)
    dni =  models.CharField(max_length=8,unique= True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.estudiante.usuario.username}"

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_rol

class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return self.username

    @property
    def is_rol_admin(self):
        return self.rol.is_admin if self.rol else False
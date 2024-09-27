from django.db import models

# Create your models here.
class Curso(models.Model):
    codigo = models.CharField(max_length=10, unique=True)  # Campo único
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    creditos = models.IntegerField()
    pre_requisitos = models.ManyToManyField('self', symmetrical=False, related_name='requisitos_para', blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

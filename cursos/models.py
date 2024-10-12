from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from estudiantes.models import Estudiante 
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

class Curso(models.Model):
    codigo = models.CharField(max_length=10, unique=True)  # Campo único
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    creditos = models.IntegerField()
    ciclo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pre_requisitos = models.ManyToManyField('self', symmetrical=False, related_name='requisitos_para', blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre} (Ciclo {self.ciclo})"

    

class HistorialNotas(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='historial_notas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='historial_notas')
    nota = models.DecimalField(max_digits=5, decimal_places=2)  # Campo para la nota
    semestre = models.ForeignKey('semestre.Semestre', on_delete=models.CASCADE, related_name='historial_notas')  # Usa la cadena aquí también
    class Meta:
        unique_together = ('estudiante', 'curso','semestre')
    
    def __str__(self):
        return f"{self.estudiante.usuario.username} - {self.curso.nombre} - {self.nota}"

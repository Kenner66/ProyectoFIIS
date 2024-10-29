# Create your models here.
from django.db import models
from cursos.models import Curso

class Semestre(models.Model):
    PERIODO_CHOICES = (
        ('I', 'Primero'),
        ('II', 'Segundo'),
    )

    año = models.PositiveIntegerField()  # Por ejemplo, 2024
    periodo = models.CharField(max_length=2, choices=PERIODO_CHOICES)  # I o II
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.BooleanField(default=False)  # Indica si el semestre está activo

    class Meta:
        unique_together = ('año', 'periodo')  # Evita duplicados de año y periodo

    def __str__(self):
        return f"{self.año} - {self.periodo}"
    
    def cursos_disponibles_para_semestre(self):
    # Si el periodo es "II", devolver solo cursos de ciclos pares
        if self.periodo == 'II':
            cursos_disponibles = Curso.objects.filter(ciclo__in=[2, 4, 6, 8, 10])
        else:
            cursos_disponibles = Curso.objects.all()  # O cursos de ciclos impares según la lógica
        return cursos_disponibles
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

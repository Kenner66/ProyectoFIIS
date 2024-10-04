from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from estudiantes.models import Estudiante 
# Create your models here.
class Curso(models.Model):
    codigo = models.CharField(max_length=10, unique=True)  # Campo único
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    creditos = models.IntegerField()
    ciclo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pre_requisitos = models.ManyToManyField('self', symmetrical=False, related_name='requisitos_para', blank=True)
    def clean(self):
        # Si el curso pertenece al ciclo 1, no puede tener prerrequisitos
        if self.ciclo == 1 and self.pre_requisitos.exists():
            raise ValidationError("Los cursos del ciclo 1 no pueden tener prerrequisitos.")

    def __str__(self):
        return f"{self.codigo} - {self.nombre} (Ciclo {self.ciclo})"

class HistorialNotas(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='historial_notas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='historial_notas')
    nota = models.DecimalField(max_digits=5, decimal_places=2)  # Campo para la nota
    semestre = models.CharField(max_length=10)  # Ejemplo: "2023-1", "2023-2"
    
    class Meta:
        unique_together = ('estudiante', 'curso', 'semestre')
    
    def __str__(self):
        return f"{self.estudiante.usuario.username} - {self.curso.nombre} - {self.nota}"

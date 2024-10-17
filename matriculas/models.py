from django.db import models
from estudiantes.models import Estudiante
from semestre.models import Semestre
from horarios.models import Seccion
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your models here.
class Matricula(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activa = models.BooleanField(default=True)  
    class Meta:
        unique_together = ('estudiante', 'semestre') 

    def __str__(self):
        return f"{self.estudiante.usuario.username} - {self.semestre.nombre} - {'Activa' if self.es_activa() else 'Inactiva'}"

    def clean(self):
        # Verifica si el estudiante ya tiene una matrícula en el mismo semestre
        if Matricula.objects.filter(estudiante=self.estudiante, semestre=self.semestre).exists():
            raise ValidationError(f"El estudiante {self.estudiante.usuario.username} ya está matriculado en el semestre {self.semestre.nombre}.")

class MatriculaCurso(models.Model):
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('matricula', 'seccion')

    def __str__(self):
        return f"{self.matricula.estudiante.usuario.username} - {self.seccion.curso.nombre} - {self.seccion.nombre}"

    def clean(self):
        # Verificar si la sección ya está ocupada por otra matrícula del mismo estudiante
        if MatriculaCurso.objects.filter(matricula__estudiante=self.matricula.estudiante, seccion=self.seccion).exists():
            raise ValidationError(f"El estudiante ya está matriculado en la sección {self.seccion.nombre}.")

    def save(self, *args, **kwargs):
        self.clean()  # Llama a la validación antes de guardar
        super().save(*args, **kwargs)
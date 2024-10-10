from django.db import models
from cursos.models import Curso
from profesores.models import Profesor 
from semestre.models import Semestre
from django.core.exceptions import ValidationError
# Create your models here.
class Seccion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=10)
    cupos_totales = models.IntegerField()
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='secciones')
    def __str__(self):
        return f"{self.curso.nombre} - Sección {self.nombre}"

class Horario(models.Model):
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
    ]

    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=10, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('profesor', 'seccion', 'dia_semana', 'hora_inicio', 'hora_fin')
        verbose_name_plural = "Horarios"

    def __str__(self):
        return f"{self.seccion} - {self.profesor} - {self.dia_semana} {self.hora_inicio} - {self.hora_fin}"

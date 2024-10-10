'''
from django import forms
from .models import Matricula, MatriculaCurso, Curso, Seccion
from estudiantes.models import Estudiante  # Asegúrate de que el modelo Estudiante esté importado

class MatriculaForm(forms.ModelForm):
    estudiante = forms.ModelChoiceField(
        queryset=Estudiante.objects.all(),
        required=True,
        label="Selecciona el Estudiante"
    )
    
    cursos = forms.ModelMultipleChoiceField(
        queryset=Curso.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecciona los Cursos"
    )
    
    class Meta:
        model = Matricula
        fields = ['estudiante', 'semestre']  # Ahora incluye el estudiante y el semestre

class MatriculaCursoForm(forms.ModelForm):
    class Meta:
        model = MatriculaCurso
        fields = ['curso', 'seccion']  # Campos que usaremos para matricular a un curso
'''
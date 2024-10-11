
from django import forms
from .models import Matricula, MatriculaCurso,Seccion
from estudiantes.models import Estudiante  # Asegúrate de que el modelo Estudiante esté importado

class MatriculaForm(forms.ModelForm):
    codigo_estudiante = forms.CharField(
        max_length=10,
        label='Código del Estudiante',
        required=True
    )

    
    secciones = forms.ModelMultipleChoiceField(
        queryset=Seccion.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecciona las Secciones"
    )
    
    class Meta:
        model = Matricula
        fields = ['estudiante', 'semestre']  # Estudiante y semestre están bien

class MatriculaCursoForm(forms.ModelForm):
    class Meta:
        model = MatriculaCurso
        fields = ['seccion']
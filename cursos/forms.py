from django import forms
from .models import Curso,HistorialNotas,Estudiante

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['codigo', 'nombre', 'descripcion', 'creditos', 'ciclo', 'pre_requisitos']

    def __init__(self, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.ciclo == 1:
            # Deshabilitar el campo de prerrequisitos si el ciclo es 1
            self.fields['pre_requisitos'].widget.attrs['disabled'] = True

class HistorialNotasForm(forms.ModelForm):
    class Meta:
        model = HistorialNotas
        fields = ['curso', 'semestre', 'nota']




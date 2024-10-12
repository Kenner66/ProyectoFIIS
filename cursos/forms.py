from django import forms
from .models import Curso,HistorialNotas,Estudiante
from django import forms
from .models import Curso
from django.core.exceptions import ValidationError

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['codigo', 'nombre', 'descripcion', 'creditos', 'ciclo', 'pre_requisitos']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar el campo de prerequisitos por defecto
        self.fields['pre_requisitos'].widget.attrs['disabled'] = 'disabled'

    def clean(self):
        cleaned_data = super().clean()
        ciclo = cleaned_data.get('ciclo')
        pre_requisitos = cleaned_data.get('pre_requisitos')

        # Verificar si el ciclo es 1 y si se han proporcionado prerequisitos
        if ciclo == 1 and pre_requisitos:
            raise forms.ValidationError("Los cursos del ciclo 1 no pueden tener prerrequisitos.")

        return cleaned_data

    def save(self, commit=True):
        curso = super().save(commit=False)
        if commit:
            curso.save()  # Guarda el curso para obtener un ID
            # Si el ciclo es mayor que 1, habilitar y guardar prerequisitos
            if curso.ciclo > 1:
                prerequisitos = self.cleaned_data.get('pre_requisitos')
                curso.pre_requisitos.set(prerequisitos)  # Asigna prerequisitos
        return curso

class HistorialNotasForm(forms.ModelForm):
    class Meta:
        model = HistorialNotas
        fields = ['curso', 'semestre', 'nota']

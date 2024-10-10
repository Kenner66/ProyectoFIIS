from django import forms
from .models import Horario, Seccion

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['curso', 'profesor', 'seccion', 'dia_semana', 'hora_inicio', 'hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        curso = cleaned_data.get('curso')
        seccion = cleaned_data.get('seccion')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        # Validación para asegurarse de que la sección corresponde al curso seleccionado
        if seccion and curso and seccion.curso != curso:
            raise forms.ValidationError("La sección seleccionada no pertenece al curso elegido.")
        
        # Validación para asegurarse de que la hora de fin es posterior a la de inicio
        if hora_inicio and hora_fin and hora_fin <= hora_inicio:
            raise forms.ValidationError("La hora de fin debe ser posterior a la hora de inicio.")

        return cleaned_data


class SeccionForm(forms.ModelForm):
    class Meta:
        model = Seccion
        fields = ['curso', 'nombre', 'semestre', 'cupos_totales']

    def clean_cupos_totales(self):
        cupos_totales = self.cleaned_data.get('cupos_totales')
        if cupos_totales <= 0:
            raise forms.ValidationError("Los cupos totales deben ser un número positivo.")
        return cupos_totales

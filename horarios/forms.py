from django import forms
from .models import Horario, Seccion

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['profesor', 'seccion', 'dia_semana', 'hora_inicio', 'hora_fin']

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise forms.ValidationError("La hora de inicio no puede ser mayor o igual a la hora de fin.")

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

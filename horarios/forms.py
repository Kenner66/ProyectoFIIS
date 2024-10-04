from django import forms
from .models import Horario,Seccion

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

        # Validación para asegurarse de que la sección corresponde al curso seleccionado
        if seccion and curso and seccion.curso != curso:
            raise forms.ValidationError("La sección seleccionada no pertenece al curso elegido.")

        return cleaned_data
class SeccionForm(forms.ModelForm):
    class Meta:
        model = Seccion
        fields = ['curso', 'nombre', 'semestre','cupos_totales']
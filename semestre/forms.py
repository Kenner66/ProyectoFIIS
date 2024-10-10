from django import forms
from .models import Semestre

class SemestreForm(forms.ModelForm):
    class Meta:
        model = Semestre
        fields = ['año', 'periodo', 'fecha_inicio', 'fecha_fin', 'estado']

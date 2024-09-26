from django import forms
from .models import Estudiante
from usuarios.models import Usuario

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['usuario', 'codigo','base', 'carrera','activo']

    def __init__(self, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        # Filtra para mostrar solo los usuarios que tienen rol de "Estudiante"
        self.fields['usuario'].queryset = Usuario.objects.filter(rol__nombre_rol="Estudiante")
from django import forms
from .models import Estudiante,InformacionPersonal
from usuarios.models import Usuario 
class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['usuario', 'codigo', 'base', 'carrera', 'activo']

    def __init__(self, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        # Filtra para mostrar solo los usuarios que no están ya registrados como estudiantes
        estudiantes = Estudiante.objects.values_list('usuario_id', flat=True)
        self.fields['usuario'].queryset = Usuario.objects.filter(rol__nombre_rol="Estudiante").exclude(id__in=estudiantes)


class InformacionPersonalForm(forms.ModelForm):
    class Meta:
        model = InformacionPersonal
        fields = ['dni', 'nombre', 'apellido', 'fecha_nacimiento']

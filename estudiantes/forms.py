from django import forms
from .models import Estudiante,InformacionPersonal
from usuarios.models import Usuario 
from django.db.models import Q

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['usuario', 'codigo', 'base', 'carrera', 'activo']

    def __init__(self, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        estudiantes = Estudiante.objects.values_list('usuario_id', flat=True)
        
        # Si el formulario es para editar un estudiante ya existente
        if self.instance and self.instance.pk:
            # Mostrar solo usuarios que tienen el rol de estudiante, excluyendo aquellos que ya están registrados como estudiantes
            # pero incluyendo el usuario actual del estudiante que se está editando
            self.fields['usuario'].queryset = Usuario.objects.filter(
                Q(rol__nombre_rol="Estudiante") &
                (Q(id=self.instance.usuario.id) | ~Q(id__in=estudiantes))
            )
        else:
            # Si es un nuevo registro, excluir los usuarios que ya están registrados como estudiantes
            self.fields['usuario'].queryset = Usuario.objects.filter(
                rol__nombre_rol="Estudiante"
            ).exclude(id__in=estudiantes)


class InformacionPersonalForm(forms.ModelForm):
    class Meta:
        model = InformacionPersonal
        fields = ['dni', 'nombre', 'apellido', 'fecha_nacimiento']

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Rol

class UsuarioCreationForm(UserCreationForm):
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), required=True)  # Campo para seleccionar el rol

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol', 'password1', 'password2']  # Asegúrate de incluir todos los campos

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Se establece la contraseña
        if commit:
            user.save()
        return user

class CSVUploadForm(forms.Form):
    file = forms.FileField(label='Seleccionar archivo CSV')
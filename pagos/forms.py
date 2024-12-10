from django import forms

class VerificarPagoForm(forms.Form):
    numero_operacion = forms.CharField(
        label="Número de Operación",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de operación'}),
        required=True
    )

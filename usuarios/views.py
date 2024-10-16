from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import UsuarioCreationForm
from .decorators import role_required 
from estudiantes.models import Estudiante
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

from django.shortcuts import render, redirect, get_object_or_404
# Create your view
@login_required
def home(request):
    return render(request, "home.html")

@login_required
@role_required('Administrador')
def home_admin(request):
    return render(request, "home_admin.html")  # Home para el administrador

@login_required
@role_required('Estudiante')
def home_estudiante(request):
    # Asegúrate de que el usuario esté autenticado
    if request.user.is_authenticated:
        try:
            # Obtiene el estudiante asociado al usuario actual
            estudiante = Estudiante.objects.get(usuario=request.user)
            info_personal = estudiante.informacionpersonal  # Accede a la información personal
        except Estudiante.DoesNotExist:
            info_personal = None
        
        return render(request, 'home_estudiante.html', {'info_personal': info_personal})
    else:
        # Redirigir a la página de inicio de sesión o a donde desees
        return redirect('login')  # Home para el estudiante

def signin(request):
    if request.user.is_authenticated:
        # Redirige según el rol del usuario autenticado
        if request.user.is_rol_admin:  # Si es administrador
            return redirect('home_admin')
        else:  # Asumimos que es estudiante
            return redirect('home_estudiante')
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or password is incorrect",
                },
            )
        else:
            login(request, user)
            # Verifica si el usuario es admin o estudiante
            if user.is_rol_admin:  # Si es administrador
                return redirect('home_admin')  # Redirige a home_admin
            else:
                return redirect('home_estudiante')  # Redirige a home_estudiante si es estudiante
    
@login_required
def signout(request):
    logout(request)
    return redirect("signin")

@login_required
@role_required('Administrador')
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Guardamos el nuevo usuario, pero no iniciamos sesión con él
            return redirect('home_admin')  # Redirige directamente al home-admin
    else:
        form = UsuarioCreationForm()  # Si es GET, muestra el formulario vacío

    return render(request, 'registrar_usuario.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')  
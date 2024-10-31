from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import UsuarioCreationForm
from .decorators import role_required 
from estudiantes.models import Estudiante
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
# Create your view
import csv
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import CSVUploadForm
from .models import Usuario, Rol
import secrets
import string


def generar_contraseña(length=10):
    """Genera una contraseña aleatoria de longitud especificada."""
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contraseña = ''.join(secrets.choice(caracteres) for _ in range(length))
    return contraseña
@login_required
@role_required('Administrador')
def cargar_usuarios_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')  # Usa get para evitar MultiValueDictKeyError
        if not csv_file:
            messages.error(request, 'Por favor, sube un archivo CSV.')
            return render(request, 'cargar_usuarios_csv.html')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo subido no es un archivo CSV.')
            return render(request, 'cargar_usuarios_csv.html')

        # Leer el archivo CSV
        file_data = csv_file.read().decode('utf-8')
        lines = file_data.splitlines()
        reader = csv.DictReader(lines)

        for row in reader:
            username = row['username']
            email = row['email']
            rol_nombre = row['rol']

            # Obtener el rol correspondiente
            try:
                rol = Rol.objects.get(nombre_rol=rol_nombre)
            except Rol.DoesNotExist:
                messages.error(request, f'El rol "{rol_nombre}" no existe.')
                continue  # Saltar al siguiente registro si el rol no existe
            
            if Usuario.objects.filter(username=username).exists():
                messages.warning(request, f'El usuario "{username}" ya existe y se omitirá.')
                continue 
            # Crear el nuevo usuario
            usuario = Usuario(username=username, email=email, rol=rol)
            usuario.set_password(generar_contraseña())  # Generar una contraseña
            usuario.save()

        messages.success(request, 'Usuarios cargados exitosamente.')

    return render(request, 'cargar_usuarios_csv.html')


@login_required
@role_required('Administrador')
def home_admin(request):
    return render(request, "home_admin.html")  # Home para el administrador

@login_required
@role_required('Director')
def home_director(request):
    return render(request, "home_director.html")  # Home para el administrador

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
        elif request.user.rol.nombre_rol == "Director":  # Si es director
            return redirect('home_director')
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
            elif request.user.rol.nombre_rol == "Director":  # Si es supervisor
                return redirect('home_director')
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
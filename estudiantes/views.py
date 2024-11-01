from django.shortcuts import render, redirect, get_object_or_404
from .models import Estudiante,InformacionPersonal
from .forms import EstudianteForm,InformacionPersonalForm
from django.contrib.auth.decorators import login_required
from usuarios.decorators import role_required 
from django.contrib import messages
from usuarios.models import Usuario,Rol
from django.core.paginator import Paginator
import string
import secrets

import csv
def generar_contraseña(length=10):
    """Genera una contraseña aleatoria de longitud especificada."""
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contraseña = ''.join(secrets.choice(caracteres) for _ in range(length))
    return contraseña
@login_required
@role_required('Administrador')
def cargar_estudiantes_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            messages.error(request, 'Por favor, sube un archivo CSV.')
            return render(request, 'estudiantes/cargar_estudiantes_csv.html')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo subido no es un archivo CSV.')
            return render(request, 'estudiantes/cargar_estudiantes_csv.html')

        # Leer el archivo CSV
        file_data = csv_file.read().decode('utf-8')
        lines = file_data.splitlines()
        reader = csv.DictReader(lines)

        for row in reader:
            username = row['username']
            email = row['email']
            rol_nombre = row['rol']
            codigo = row['codigo']

            # Obtener o crear el usuario
            usuario, created = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'rol': Rol.objects.get_or_create(nombre_rol=rol_nombre)[0],
                }
            )

            if created:
                # Si el usuario es nuevo, generamos una contraseña y lo guardamos
                usuario.set_password(generar_contraseña())
                usuario.save()
                messages.info(request, f'Usuario "{username}" creado.')

            # Crear o actualizar el estudiante
            estudiante, estudiante_created = Estudiante.objects.get_or_create(
                usuario=usuario,
                defaults={
                    'codigo': codigo,
                    'base': row['base'],
                    'carrera': row['carrera'],
                    'activo': row.get('activo', 'True') == 'True',
                }
            )

            if estudiante_created:
                # Crear la información personal asociada al estudiante
                informacion_personal = InformacionPersonal(
                    estudiante=estudiante,
                    dni=row['dni'],
                    nombre=row['nombre'],
                    apellido=row['apellido'],
                    fecha_nacimiento=row['fecha_nacimiento']
                )
                informacion_personal.save()
                messages.info(request, f'Estudiante con código "{codigo}" creado.')
            else:
                messages.warning(request, f'El estudiante con código "{codigo}" ya existe y se omitió.')

        messages.success(request, 'Usuarios y estudiantes cargados exitosamente.')

    return render(request, 'estudiantes/cargar_estudiantes_csv.html')


@login_required
@role_required('Administrador')
def listar_estudiantes(request):
    estudiantes = Estudiante.objects.all().order_by('id') # Obtiene todos los estudiantes
    paginator = Paginator(estudiantes, 5) 
    page_number = request.GET.get('page')
    estudiantes = paginator.get_page(page_number)
    return render(request, 'estudiantes/listar_estudiantes.html', {'estudiantes': estudiantes})

@login_required
@role_required('Administrador')
def agregar_estudiante(request):
    if request.method == 'POST':
        if 'cancelar' in request.POST:
            return redirect('listar_estudiantes')
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_estudiantes')
    else:
        form = EstudianteForm()

    return render(request, 'estudiantes/agregar_estudiante.html', {'form': form})

@login_required
@role_required('Administrador')
def editar_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == 'POST':
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            return redirect('listar_estudiantes')
    else:
        form = EstudianteForm(instance=estudiante)
    return render(request, 'estudiantes/editar_estudiante.html', {'form': form})

@login_required
@role_required('Administrador')
def agregar_informacion_personal(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    
    if request.method == 'POST':
        form = InformacionPersonalForm(request.POST)
        if form.is_valid():
            info_personal = form.save(commit=False)
            info_personal.estudiante = estudiante  # Vincula la información con el estudiante
            info_personal.save()
            return redirect('listar_estudiantes')  # Cambia según tu URL
    else:
        form = InformacionPersonalForm()
    
    return render(request, 'estudiantes/agregar_informacion_personal.html', {'form': form, 'estudiante': estudiante})

@login_required
@role_required('Administrador')
def ver_informacion_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    informacion_personal = InformacionPersonal.objects.filter(estudiante=estudiante).first()
    return render(request, 'estudiantes/ver_informacion_estudiante.html', {'estudiante': estudiante, 'informacion_personal': informacion_personal})

@login_required
@role_required('Administrador')
def editar_informacion_personal(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    info_personal = get_object_or_404(InformacionPersonal, estudiante=estudiante)

    if request.method == 'POST':
        form = InformacionPersonalForm(request.POST, instance=info_personal)
        if form.is_valid():
            form.save()
            return redirect('listar_estudiantes')  # Cambia según tu URL
    else:
        form = InformacionPersonalForm(instance=info_personal)

    return render(request, 'estudiantes/editar_informacion_personal.html', {'form': form, 'estudiante': estudiante})



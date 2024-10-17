from django.shortcuts import render, redirect, get_object_or_404
from .models import Estudiante,InformacionPersonal
from .forms import EstudianteForm,InformacionPersonalForm
from django.contrib.auth.decorators import login_required
from usuarios.decorators import role_required 
from django.contrib import messages
from usuarios.models import Usuario
import csv

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
        file_data = csv_file.read().decode('latin-1')
        lines = file_data.splitlines()
        reader = csv.DictReader(lines)

        for row in reader:
            username = row['username']

            try:
                usuario = Usuario.objects.get(username=username)  # Verificar si el usuario existe
            except Usuario.DoesNotExist:
                messages.error(request, f'El usuario con username "{username}" no existe.')
                continue  # Saltar al siguiente registro si no existe el usuario

            # Verificar si el estudiante ya existe
            if Estudiante.objects.filter(codigo=row['codigo']).exists():
                estudiante = Estudiante.objects.get(codigo=row['codigo'])
                messages.warning(request, f'El estudiante con código {row["codigo"]} ya existe y se omitirá.')
                continue  # O, si prefieres, puedes actualizar el estudiante en lugar de omitirlo
            
            try:
                # Crear el nuevo estudiante
                estudiante = Estudiante(
                    usuario=usuario,
                    codigo=row['codigo'],
                    base=row['base'],
                    carrera=row['carrera'],
                    activo=row.get('activo', 'True') == 'True'
                )
                estudiante.save()

                # Crear la información personal
                informacion_personal = InformacionPersonal(
                    estudiante=estudiante,
                    dni=row['dni'],
                    nombre=row['nombre'],
                    apellido=row['apellido'],
                    fecha_nacimiento=row['fecha_nacimiento']
                )
                informacion_personal.save()

            except Exception as e:
                messages.error(request, f'Error al crear estudiante para "{username}": {str(e)}')
                continue

        messages.success(request, 'Estudiantes cargados exitosamente.')
    return render(request, 'estudiantes/cargar_estudiantes_csv.html')


@login_required
@role_required('Administrador')
def listar_estudiantes(request):
    estudiantes = Estudiante.objects.all()  # Obtiene todos los estudiantes
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



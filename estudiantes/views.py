from django.shortcuts import render, redirect, get_object_or_404
from .models import Estudiante,InformacionPersonal
from .forms import EstudianteForm,InformacionPersonalForm
from django.contrib.auth.decorators import login_required
from usuarios.decorators import role_required 
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



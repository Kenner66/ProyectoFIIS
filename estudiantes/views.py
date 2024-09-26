from django.shortcuts import render, redirect, get_object_or_404
from .models import Estudiante
from .forms import EstudianteForm
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
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estudiantes/listar_estudiantes')
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
            return redirect('estudiantes/listar_estudiantes')
    else:
        form = EstudianteForm(instance=estudiante)
    return render(request, 'estudiantes/editar_estudiante.html', {'form': form})
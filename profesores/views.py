
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profesor
from .forms import ProfesorForm
from django.contrib.auth.decorators import login_required
from usuarios.decorators import role_required

@login_required
@role_required('Administrador')
def listar_profesores(request):
    profesores = Profesor.objects.all()
    return render(request, 'profesores/listar_profesores.html', {'profesores': profesores})

@login_required
@role_required('Administrador')
def agregar_profesor(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_profesores')
    else:
        form = ProfesorForm()
    return render(request, 'profesores/agregar_profesor.html', {'form': form})

@login_required
@role_required('Administrador')
def editar_profesor(request, profesor_id):
    profesor = get_object_or_404(Profesor, pk=profesor_id)
    if request.method == 'POST':
        form = ProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            return redirect('listar_profesores')
    else:
        form = ProfesorForm(instance=profesor)
    return render(request, 'profesores/editar_profesor.html', {'form': form, 'profesor': profesor})

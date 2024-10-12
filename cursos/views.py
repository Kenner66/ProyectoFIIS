
from django.shortcuts import render,redirect, get_object_or_404
from .models import Curso,HistorialNotas
from estudiantes.models import Estudiante
from .forms import CursoForm,HistorialNotasForm
from django.contrib.auth.decorators import login_required
from usuarios.decorators import role_required 
from django.core.exceptions import ValidationError
@login_required
@role_required('Administrador')
def listar_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos/listar_cursos.html', {'cursos': cursos})

@login_required
@role_required('Administrador')
def agregar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()  # Llama al método save del formulario
            return redirect('listar_cursos')  # Redirigir después de guardar
    else:
        form = CursoForm()

    return render(request, 'cursos/agregar_curso.html', {'form': form})

@login_required
@role_required('Administrador')
def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('listar_cursos')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'cursos/editar_curso.html', {'form': form})

@login_required
@role_required('Administrador')
def listar_estudiantes_historial(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'estudiantes/listar_estudiantes_historial.html', {'estudiantes': estudiantes})


@login_required
@role_required('Administrador')
def agregar_nota(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)

    if request.method == 'POST':
        form = HistorialNotasForm(request.POST)
        if form.is_valid():
            nueva_nota = form.save(commit=False)
            curso = nueva_nota.curso

            # Obtener los prerrequisitos del curso actual
            pre_requisitos = curso.pre_requisitos.all()

            # Verificar si el estudiante ha aprobado todos los prerrequisitos
            for pre_requisito in pre_requisitos:
                historial_pre_req = HistorialNotas.objects.filter(
                    estudiante=estudiante, 
                    curso=pre_requisito, 
                    nota__gte=10.5  # Suponiendo que la nota mínima para aprobar es 10.5
                )
                if not historial_pre_req.exists():
                    # Si el estudiante no ha aprobado un prerequisito, mostrar un error
                    form.add_error(None, f"El estudiante no ha aprobado el prerrequisito: {pre_requisito.nombre}")
                    return render(request, 'estudiantes/agregar_nota.html', {'form': form, 'estudiante': estudiante})

            # Si ha aprobado todos los prerrequisitos, guardar la nota
            nueva_nota.estudiante = estudiante
            nueva_nota.save()
            return redirect('historial_notas_estudiante', estudiante_id=estudiante_id)
    else:
        form = HistorialNotasForm()

    return render(request, 'estudiantes/agregar_nota.html', {'form': form, 'estudiante': estudiante})

@login_required
@role_required('Administrador')
def historial_notas_estudiante(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
    historial = estudiante.historial_notas.all()  # Obtiene todas las notas del estudiante

    context = {
        'estudiante': estudiante,
        'historial': historial,  # Solo se muestra el historial aquí
    }
    return render(request, 'estudiantes/historial_notas_estudiante.html', context)


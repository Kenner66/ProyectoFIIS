
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Horario,Seccion
from .forms import HorarioForm,SeccionForm
from cursos.models import Curso
from profesores.models import Profesor
from django.contrib.auth.decorators import login_required
from usuarios.decorators import role_required 

@login_required
@role_required('Administrador')
def listar_horarios(request):
    horarios = Horario.objects.all()
    return render(request, 'horarios/listar_horarios.html', {'horarios': horarios})

@login_required
@role_required('Administrador')
def agregar_horario(request):
    if request.method == 'POST':
        # Obtenemos los datos de los campos en forma de lista
        dias = request.POST.getlist('dia_semana[]')
        horas_inicio = request.POST.getlist('hora_inicio[]')
        horas_fin = request.POST.getlist('hora_fin[]')

        # Obtener las instancias de curso, profesor y sección solo una vez
        curso = Curso.objects.get(pk=request.POST['curso'])  # Obtener la instancia del curso
        profesor = Profesor.objects.get(pk=request.POST['profesor'])  # Obtener la instancia del profesor
        seccion = Seccion.objects.get(pk=request.POST['seccion'])  # Obtener la instancia de la sección

        for dia, hora_inicio, hora_fin in zip(dias, horas_inicio, horas_fin):
            # Crear el nuevo horario con las instancias correctas
            nuevo_horario = Horario(
                curso=curso,
                profesor=profesor,
                seccion=seccion,
                dia_semana=dia,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin
            )
            nuevo_horario.save()

        return redirect('listar_horarios')  # Redirigir a la lista de horarios

    form = HorarioForm()
    return render(request, 'horarios/agregar_horario.html', {'form': form})


@login_required
@role_required('Administrador') 
def editar_horario(request, horario_id):
    horario = get_object_or_404(Horario, id=horario_id)
    
    # Obtener todos los horarios asociados al mismo curso y sección
    horarios = Horario.objects.filter(curso=horario.curso, seccion=horario.seccion)

    if request.method == 'POST':
        # Obtener las listas de horas y días del formulario
        dias = request.POST.getlist('dia_semana[]')
        horas_inicio = request.POST.getlist('hora_inicio[]')
        horas_fin = request.POST.getlist('hora_fin[]')

        # Validar que las listas tengan la misma longitud
        if len(dias) == len(horas_inicio) == len(horas_fin):
            # Limpiar los horarios existentes para evitar duplicados
            horarios.delete()

            # Crear y guardar los nuevos horarios
            for dia, hora_inicio, hora_fin in zip(dias, horas_inicio, horas_fin):
                nuevo_horario = Horario(
                    curso=horario.curso,
                    profesor=horario.profesor,
                    seccion=horario.seccion,
                    dia_semana=dia,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin
                )
                nuevo_horario.save()

            return redirect('listar_horarios')  # Redirigir a la lista de horarios
    else:
        # Si no es POST, simplemente muestra los horarios para editar
        form = HorarioForm(instance=horario)

    return render(request, 'horarios/editar_horario.html', {'form': form, 'horarios': horarios})



@login_required
@role_required('Administrador') 
def listar_secciones(request):
    secciones = Seccion.objects.all()
    return render(request, 'secciones/listar_secciones.html', {'secciones': secciones})

@login_required
@role_required('Administrador')
def agregar_seccion(request):
    if request.method == 'POST':
        form = SeccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_secciones')
    else:
        form = SeccionForm()
    return render(request, 'secciones/agregar_seccion.html',  {'form': form})

@login_required
@role_required('Administrador')
def editar_seccion(request, seccion_id):
    seccion = get_object_or_404(Seccion, pk=seccion_id)
    if request.method == 'POST':
        form = SeccionForm(request.POST, instance=seccion)
        if form.is_valid():
            form.save()
            return redirect('listar_secciones')
    else:
        form = SeccionForm(instance=seccion)
    return render(request, 'secciones/editar_seccion.html', {'form': form})
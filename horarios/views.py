
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
        dias = request.POST.getlist('dia_semana[]')
        horas_inicio = request.POST.getlist('hora_inicio[]')
        horas_fin = request.POST.getlist('hora_fin[]')

        curso = Curso.objects.get(pk=request.POST['curso'])
        profesor = Profesor.objects.get(pk=request.POST['profesor'])
        seccion = Seccion.objects.get(pk=request.POST['seccion'])

        # Validar que las horas de inicio y fin son correctas
        errores = []
        horarios_a_crear = []
        for dia, hora_inicio, hora_fin in zip(dias, horas_inicio, horas_fin):
            if hora_inicio >= hora_fin:
                errores.append(f"El horario de {dia} tiene una hora de inicio posterior o igual a la hora de fin.")
            else:
                nuevo_horario = Horario(
                    curso=curso,
                    profesor=profesor,
                    seccion=seccion,
                    dia_semana=dia,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin
                )
                horarios_a_crear.append(nuevo_horario)

        if errores:
            return render(request, 'horarios/agregar_horario.html', {'errores': errores})

        # Usar bulk_create para crear todos los horarios de una vez
        Horario.objects.bulk_create(horarios_a_crear)
        return redirect('listar_horarios')

    form = HorarioForm()
    return render(request, 'horarios/agregar_horario.html', {'form': form})

@login_required
@role_required('Administrador') 
def editar_horario(request, horario_id):
    horario = get_object_or_404(Horario, id=horario_id)
    
    # Obtener todos los horarios asociados al mismo curso y sección
    horarios = Horario.objects.filter(curso=horario.curso, seccion=horario.seccion)

    # Obtener todos los profesores
    profesores = Profesor.objects.all()

    if request.method == 'POST':
        dias = request.POST.getlist('dia_semana[]')
        horas_inicio = request.POST.getlist('hora_inicio[]')
        horas_fin = request.POST.getlist('hora_fin[]')
        profesor = Profesor.objects.get(pk=request.POST['profesor'])  # Obtener el nuevo profesor

        if len(dias) == len(horas_inicio) == len(horas_fin):
            horarios.delete()

            for dia, hora_inicio, hora_fin in zip(dias, horas_inicio, horas_fin):
                nuevo_horario = Horario(
                    curso=horario.curso,
                    profesor=profesor,  # Asignar el nuevo profesor
                    seccion=horario.seccion,
                    dia_semana=dia,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin
                )
                nuevo_horario.save()

            return redirect('listar_horarios')
    else:
        form = HorarioForm(instance=horario)

    return render(request, 'horarios/editar_horario.html', {
        'form': form, 
        'horarios': horarios, 
        'profesores': profesores  # Pasar profesores al template
    })




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
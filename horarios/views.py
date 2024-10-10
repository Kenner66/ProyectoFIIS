# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Horario, Seccion
from .forms import HorarioForm, SeccionForm
from cursos.models import Curso
from profesores.models import Profesor
from django.contrib.auth.decorators import login_required
from usuarios.decorators import role_required
from django.contrib import messages

@login_required
@role_required('Administrador')
def listar_horarios(request):
    horarios = Horario.objects.all()
    return render(request, 'horarios/listar_horarios.html', {'horarios': horarios})

@login_required
@role_required('Administrador')
def agregar_horario(request):
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            dias = request.POST.getlist('dia_semana[]')
            horas_inicio = request.POST.getlist('hora_inicio[]')
            horas_fin = request.POST.getlist('hora_fin[]')

            # Obtener instancias del curso, profesor y sección
            curso = form.cleaned_data['curso']
            profesor = form.cleaned_data['profesor']
            seccion = form.cleaned_data['seccion']

            errores = []
            horarios_a_crear = []

            # Validar que las horas de inicio y fin son correctas
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
                for error in errores:
                    messages.error(request, error)
                return render(request, 'horarios/agregar_horario.html', {'form': form})

            # Usar bulk_create para crear todos los horarios de una vez
            Horario.objects.bulk_create(horarios_a_crear)
            messages.success(request, "Horarios agregados exitosamente.")
            return redirect('listar_horarios')

    else:
        form = HorarioForm()
    
    return render(request, 'horarios/agregar_horario.html', {'form': form})

@login_required
@role_required('Administrador')
def editar_horario(request, horario_id):
    horario = get_object_or_404(Horario, id=horario_id)

    if request.method == 'POST':
        form = HorarioForm(request.POST, instance=horario)
        if form.is_valid():
            # Obtener nuevos datos
            dias = request.POST.getlist('dia_semana[]')
            horas_inicio = request.POST.getlist('hora_inicio[]')
            horas_fin = request.POST.getlist('hora_fin[]')
            profesor = form.cleaned_data['profesor']  # Obtener el nuevo profesor

            # Validar que las horas de inicio y fin son correctas
            horarios_a_actualizar = []
            errores = []
            for dia, hora_inicio, hora_fin in zip(dias, horas_inicio, horas_fin):
                if hora_inicio >= hora_fin:
                    errores.append(f"El horario de {dia} tiene una hora de inicio posterior o igual a la hora de fin.")
                else:
                    nuevo_horario = Horario(
                        curso=horario.curso,
                        profesor=profesor,
                        seccion=horario.seccion,
                        dia_semana=dia,
                        hora_inicio=hora_inicio,
                        hora_fin=hora_fin
                    )
                    horarios_a_actualizar.append(nuevo_horario)

            if errores:
                for error in errores:
                    messages.error(request, error)
                return render(request, 'horarios/editar_horario.html', {
                    'form': form, 
                    'horario': horario
                })

            # Eliminar horarios antiguos y agregar los nuevos
            horario.delete()
            Horario.objects.bulk_create(horarios_a_actualizar)
            messages.success(request, "Horarios actualizados exitosamente.")
            return redirect('listar_horarios')
    else:
        form = HorarioForm(instance=horario)

    return render(request, 'horarios/editar_horario.html', {
        'form': form, 
        'horario': horario
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
            messages.success(request, "Sección agregada exitosamente.")
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
            messages.success(request, "Sección editada exitosamente.")
            return redirect('listar_secciones')
    else:
        form = SeccionForm(instance=seccion)
    return render(request, 'secciones/editar_seccion.html', {'form': form})

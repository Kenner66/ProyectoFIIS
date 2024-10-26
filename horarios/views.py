# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Horario, Seccion
from .forms import HorarioForm, SeccionForm
from cursos.models import Curso
from profesores.models import Profesor
from django.contrib.auth.decorators import login_required
from usuarios.decorators import role_required
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator

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
        profesor_id = request.POST.get('profesor')
        seccion_id = request.POST.get('seccion')

        for dia, hora_inicio, hora_fin in zip(dias, horas_inicio, horas_fin):
            horario = Horario(
                profesor_id=profesor_id,
                seccion_id=seccion_id,
                dia_semana=dia,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin
            )
            horario.save()

        return redirect('listar_horarios')

    else:
        form = HorarioForm()

    return render(request, 'horarios/agregar_horario.html', {'form': form})


@login_required
@role_required('Administrador')
def editar_horario(request, horario_id):
    # Obtén el horario a editar
    horario = get_object_or_404(Horario, id=horario_id)

    if request.method == 'POST':
        dias = request.POST.getlist('dia_semana[]')
        horas_inicio = request.POST.getlist('hora_inicio[]')
        horas_fin = request.POST.getlist('hora_fin[]')
        profesor_id = request.POST.get('profesor')
        seccion_id = request.POST.get('seccion')

        # Borra los horarios existentes para este profesor y sección
        Horario.objects.filter(profesor_id=profesor_id, seccion_id=seccion_id).delete()

        # Guarda los nuevos horarios
        for dia, hora_inicio, hora_fin in zip(dias, horas_inicio, horas_fin):
            horario = Horario(
                profesor_id=profesor_id,
                seccion_id=seccion_id,
                dia_semana=dia,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin
            )
            horario.save()

        return redirect('listar_horarios')

    else:
        # Carga los datos existentes en el formulario
        form = HorarioForm(initial={'profesor': horario.profesor, 'seccion': horario.seccion})

        # Obtén todos los horarios relacionados con este profesor y sección
        horarios = Horario.objects.filter(profesor=horario.profesor, seccion=horario.seccion)

        # Prepara los datos para el template
        dias = [h.dia_semana for h in horarios]
        horas_inicio = [h.hora_inicio for h in horarios]
        horas_fin = [h.hora_fin for h in horarios]

    # Combina los datos en una lista de tuplas
    horario_data = list(zip(dias, horas_inicio, horas_fin))

    return render(request, 'horarios/editar_horario.html', {
        'form': form,
        'horario_data': horario_data,  # Envía los datos combinados
    })



############################################################################################
import csv
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Seccion, Curso, Semestre  # Asegúrate de importar tus modelos

@login_required
@role_required('Administrador')
def cargar_secciones_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            messages.error(request, 'Por favor, sube un archivo CSV.')
            return render(request, 'secciones/cargar_secciones_csv.html')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo subido no es un archivo CSV.')
            return render(request, 'secciones/cargar_secciones_csv.html')

        try:
            file_data = csv_file.read().decode('latin-1')  # Para manejar posibles caracteres especiales
            lines = file_data.splitlines()
            reader = csv.DictReader(lines)

            for row in reader:
                try:
                    curso = Curso.objects.get(nombre=row['curso'])  # Asegúrate de que estás buscando por el campo correcto

                    # Verifica si el semestre está presente
                    semestre_nombre = row.get('semestre')  # Obtén el semestre del CSV
                    if semestre_nombre:  # Solo busca si se proporciona el semestre
                        try:
                            semestre = Semestre.objects.get(nombre=semestre_nombre)  # Busca el semestre por su nombre
                        except Semestre.DoesNotExist:
                            messages.warning(request, f'El semestre "{semestre_nombre}" no existe. Se omitirá esta sección.')
                            continue
                    else:
                        semestre = None  # Asigna None si no se proporciona semestre

                    seccion = Seccion(
                        curso=curso,
                        nombre=row['nombre'],
                        cupos_totales=int(row['cupos_totales']),
                        semestre=semestre  # Aquí puedes dejarlo como None si no se proporciona
                    )
                    seccion.save()

                except Curso.DoesNotExist:
                    messages.warning(request, f'El curso "{row["curso"]}" no existe. Se omitirá esta sección.')
                    continue
                except Exception as e:
                    messages.error(request, f'Error al crear la sección "{row["nombre"]}": {str(e)}')
                    continue

            messages.success(request, 'Secciones cargadas exitosamente.')
            return redirect('home_admin')

        except Exception as e:
            messages.error(request, f'Ocurrió un error al procesar el archivo: {str(e)}')

    return render(request, 'secciones/cargar_secciones_csv.html')


@login_required
@role_required('Administrador')
def listar_secciones(request):
    secciones = Seccion.objects.all().order_by('curso__ciclo','nombre')
    paginator = Paginator(secciones, 8) 
    page_number = request.GET.get('page')
    secciones = paginator.get_page(page_number)
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

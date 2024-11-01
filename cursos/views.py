
from django.shortcuts import render,redirect, get_object_or_404
from .models import Curso,HistorialNotas
from estudiantes.models import Estudiante
from semestre.models import Semestre
from .forms import CursoForm,HistorialNotasForm
from django.contrib.auth.decorators import login_required
from usuarios.decorators import role_required 
from django.core.exceptions import ValidationError
import csv
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.paginator import Paginator

@login_required
@role_required('Administrador')
def cargar_historial_notas_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            messages.error(request, 'Por favor, sube un archivo CSV.')
            return render(request, 'cursos/cargar_historial_notas_csv.html')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo subido no es un archivo CSV.')
            return render(request, 'cursos/cargar_historial_notas_csv.html')

        # Leer el archivo CSV
        file_data = csv_file.read().decode('latin-1')
        lines = file_data.splitlines()
        reader = csv.DictReader(lines)

        for row in reader:
            try:
                # Obtener el estudiante, curso y semestre
                estudiante = Estudiante.objects.get(codigo=row['codigo_estudiante'])
                curso = Curso.objects.get(nombre=row['nombre_curso'])
                semestre = Semestre.objects.get(año=row['año'], periodo=row['periodo'])  # Ajuste aquí

                # Verificar si la combinación de estudiante, curso y semestre ya existe
                if HistorialNotas.objects.filter(estudiante=estudiante, curso=curso, semestre=semestre).exists():
                    messages.warning(request, f'El historial para {estudiante.usuario.username} en el curso {curso.nombre} y semestre {semestre} ya existe y se omitirá.')
                    continue  # Omitir si ya existe

                # Crear un nuevo registro de historial
                historial_nota = HistorialNotas(
                    estudiante=estudiante,
                    curso=curso,
                    nota=row['nota'],
                    semestre=semestre
                )
                historial_nota.save()

            except Estudiante.DoesNotExist:
                messages.error(request, f'El estudiante con código "{row["codigo_estudiante"]}" no existe.')
            except Curso.DoesNotExist:
                messages.error(request, f'El curso con nombre "{row["nombre_curso"]}" no existe.')
            except Semestre.DoesNotExist:
                messages.error(request, f'El semestre con año "{row["año"]}" y periodo "{row["periodo"]}" no existe.')
            except Exception as e:
                messages.error(request, f'Error al cargar historial para el estudiante con código {row["codigo_estudiante"]}: {str(e)}')

        messages.success(request, 'Historiales de notas cargados exitosamente.')
    return render(request, 'cursos/cargar_historial_notas_csv.html')


@login_required
@role_required('Administrador')
def cargar_cursos_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            messages.error(request, 'Por favor, sube un archivo CSV.')
            return render(request, 'cursos/cargar_cursos_csv.html')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo subido no es un archivo CSV.')
            return render(request, 'cursos/cargar_cursos_csv.html')

        try:
            file_data = csv_file.read().decode('latin-1')  # Para manejar posibles caracteres especiales
            lines = file_data.splitlines()
            reader = csv.DictReader(lines)

            for row in reader:
                try:
                    curso = Curso(
                        codigo=row['codigo'],
                        nombre=row['nombre'],
                        descripcion=row.get('descripcion', ''),
                        creditos=row['creditos'],
                        ciclo=row['ciclo'],
                    )
                    curso.save()

                    # Manejar prerequisitos
                    if 'pre_requisitos' in row and row['pre_requisitos']:
                        pre_requisitos_codigos = row['pre_requisitos'].split(';')
                        for codigo_pre_req in pre_requisitos_codigos:
                            try:
                                pre_requisito = Curso.objects.get(codigo=codigo_pre_req)
                                curso.pre_requisitos.add(pre_requisito)
                            except Curso.DoesNotExist:
                                messages.warning(request, f'Curso prerequisito con código {codigo_pre_req} no existe.')
                    curso.save()

                except Exception as e:
                    messages.error(request, f'Error al crear el curso {row["nombre"]}: {str(e)}')
                    continue

            messages.success(request, 'Cursos cargados exitosamente.')
            return redirect('home_admin')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al procesar el archivo: {str(e)}')

    return render(request, 'cursos/cargar_cursos_csv.html')


@login_required
@role_required('Administrador')
def listar_cursos(request):
    cursos = Curso.objects.all().order_by('ciclo')
    paginator = Paginator(cursos, 8) 
    page_number = request.GET.get('page')
    cursos = paginator.get_page(page_number)
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


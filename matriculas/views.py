from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MatriculaForm, MatriculaCursoForm
from .models import Matricula, MatriculaCurso,Seccion,Semestre  
from cursos.models import HistorialNotas,Curso
from .forms import MatriculaForm
from estudiantes.models import Estudiante,InformacionPersonal
from django.forms import formset_factory
from usuarios.decorators import role_required 
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Matricula, Seccion, Semestre
from cursos.models import HistorialNotas
from estudiantes.models import Estudiante
from django.http import JsonResponse

@login_required
@role_required('Administrador')
def listar_matriculas(request):
    matriculas = Matricula.objects.select_related('estudiante').all()
    return render(request, 'matriculas/listar_matriculas.html', {'matriculas': matriculas})

@login_required 
@role_required('Administrador')
def crear_matricula(request):
    if request.method == 'GET':
        # Si se está buscando un estudiante
        codigo_estudiante = request.GET.get('codigo_estudiante')
        if codigo_estudiante:
            estudiante = Estudiante.objects.filter(codigo=codigo_estudiante, activo=True).first()  # Filtra por activo
            if estudiante:
                return JsonResponse({
                    'nombre_estudiante': estudiante.informacionpersonal.nombre,
                    'apellido_estudiante': estudiante.informacionpersonal.apellido,  # Añadir apellido aquí
                    'codigo': estudiante.codigo
                })
            else:
                return JsonResponse({'error': 'Estudiante no encontrado o inactivo'})

        # Obtener semestres activos
        semestres = Semestre.objects.filter(estado=True)  # Aquí filtramos por estado
        return render(request, 'matriculas/crear_matricula.html', {'semestres': semestres})

    # Si se selecciona un semestre, cargar secciones
    semestre_id = request.GET.get('semestre_id')
    if semestre_id:
        secciones = Seccion.objects.filter(semestre_id=semestre_id)  # Filtra las secciones por semestre
        secciones_data = [
            {
                'id': seccion.id,
                'nombre_curso': seccion.curso.nombre,  # Asegúrate de que 'curso' tiene el campo 'nombre'
                'seccion': seccion.nombre  # Asegúrate de que 'nombre' es el campo de la sección
            }
            for seccion in secciones
        ]
        return JsonResponse(secciones_data, safe=False)

    # Si no se encuentra el semestre, devuelve un error o una respuesta vacía
    return JsonResponse({'error': 'Semestre no encontrado'}, status=404)

@login_required
@role_required('Administrador')
def cargar_secciones(request, semestre_id):
    # Filtrar las secciones según el semestre_id
    secciones = Seccion.objects.filter(semestre_id=semestre_id).values('id', 'curso__nombre', 'nombre')
    
    # Retornar las secciones en formato JSON
    return JsonResponse(list(secciones), safe=False)


def is_course_available_in_current_semester(curso, semestre_actual):
    if not semestre_actual:
        return False  # Si no hay semestre activo, no se puede matricular
    # Verificar si el curso pertenece al ciclo correcto para el semestre
    return (semestre_actual.periodo == 'I' and curso.ciclo % 2 == 1) or \
           (semestre_actual.periodo == 'II' and curso.ciclo % 2 == 0)
@login_required
@role_required('Administrador')
def validar_seccion(request, codigo_estudiante, seccion_id):
    try:
        # Obtener la sección y el estudiante
        estudiante = Estudiante.objects.get(codigo=codigo_estudiante)
        seccion = Seccion.objects.get(id=seccion_id)
        curso = seccion.curso

        # Validar si el estudiante ya aprobó el curso
        historial = HistorialNotas.objects.filter(estudiante=estudiante, curso=curso).first()

        if historial and historial.nota >= 11:  # Si ya aprobó el curso
            return JsonResponse({'error': f'El estudiante ya aprobó el curso {curso.nombre}.'})

        # Obtener la lista de secciones seleccionadas de la sesión
        secciones_seleccionadas_ids = request.session.get('secciones_seleccionadas', [])
        secciones_seleccionadas = Seccion.objects.filter(id__in=secciones_seleccionadas_ids)

        # Validar prerrequisitos específicos del curso
        prerrequisitos = curso.pre_requisitos.all()
        for prerequisito in prerrequisitos:
            # Revisar si el prerrequisito ya fue aprobado en el historial académico
            historial_prerrequisito = HistorialNotas.objects.filter(estudiante=estudiante, curso=prerequisito).first()

            if historial_prerrequisito and historial_prerrequisito.nota >= 11:
                continue  # Si ya aprobó el prerrequisito, seguimos con la validación del siguiente

            # Si no ha aprobado el prerrequisito, validar si lo seleccionó para el semestre actual o semestre anterior
            seccion_prerrequisito = secciones_seleccionadas.filter(curso=prerequisito).first()

            # Aquí añadimos la validación si el curso pertenece al semestre anterior
            if not seccion_prerrequisito:
                # Si el curso es del semestre II y el prerrequisito está siendo cursado en el semestre I, lo permitimos
                if curso.ciclo % 2 == 0:  # Si es de ciclo par (ejemplo: semestre II)
                    seccion_prerrequisito_anterior = Seccion.objects.filter(curso=prerequisito, curso__ciclo=curso.ciclo-1).first()
                    if seccion_prerrequisito_anterior:
                        continue  # Si el prerrequisito está en el semestre anterior, permitimos la matriculación

                return JsonResponse({'error': f'El estudiante no ha aprobado ni seleccionado el prerrequisito {prerequisito.nombre}.'})

        # Validar si el estudiante ya tiene esta sección del curso en su lista de secciones seleccionadas
        secciones_existentes = secciones_seleccionadas.filter(curso=curso)

        if secciones_existentes.exists():
            return JsonResponse({'error': f'El estudiante ya ha añadido una sección del curso {curso.nombre}.'})

        # Si pasó todas las validaciones
        return JsonResponse({
            'success': 'Validación exitosa, puedes añadir el curso.',
            'curso_nombre': curso.nombre,
            'seccion_nombre': seccion.nombre
        })

    except Estudiante.DoesNotExist:
        return JsonResponse({'error': 'Estudiante no encontrado.'})
    except Seccion.DoesNotExist:
        return JsonResponse({'error': 'Sección no encontrada.'})

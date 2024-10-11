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

        # Si el curso es de ciclo 1, no tiene prerrequisitos
        if curso.ciclo == 1:
            return JsonResponse({
                'success': 'Validación exitosa, puede añadir el curso.',
                'curso_nombre': curso.nombre,
                'seccion_nombre': seccion.nombre
            })

        # Validar prerrequisitos específicos del curso
        prerrequisitos = curso.pre_requisitos.all()  # Asume que pre_requisitos es ManyToManyField
        for prerequisito in prerrequisitos:
            historial_prerrequisito = HistorialNotas.objects.filter(estudiante=estudiante, curso=prerequisito).first()
            
            # Validar si ya aprobó el prerrequisito
            if historial_prerrequisito:
                if historial_prerrequisito.nota < 11:
                    return JsonResponse({'error': f'El estudiante no ha aprobado el prerrequisito {prerequisito.nombre}.'})

        # Validar si el estudiante ya tiene esta sección del curso en su lista de secciones seleccionadas
        secciones_seleccionadas_ids = request.session.get('secciones_seleccionadas', [])
        secciones_existentes = Seccion.objects.filter(id__in=secciones_seleccionadas_ids, curso=curso)

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

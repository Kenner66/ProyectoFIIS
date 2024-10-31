from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from estudiantes.models import Estudiante
from matriculas.models import Matricula, MatriculaCurso
from django.db.models import Count
import plotly.express as px
import plotly.io as pio
from cursos.models import Curso
from django.contrib.auth.decorators import login_required
from usuarios.decorators import role_required 

from django.core.paginator import Paginator

@login_required
@role_required('Administrador')
def estadisticas_generales(request):
    # Total de estudiantes matriculados únicos
    total_estudiantes = Matricula.objects.filter(activa=True).values('estudiante').distinct().count()

    # Distribución geográfica por "base" solo de estudiantes matriculados
    distribucion_geografica = (
        Estudiante.objects
        .filter(id__in=Matricula.objects.filter(activa=True).values('estudiante'))  # Filtra estudiantes matriculados
        .values('base')
        .annotate(total=Count('id'))
    )

    distribucion_geografica = list(distribucion_geografica)

    # Obtener todos los ciclos únicos
    ciclos = Curso.objects.values('ciclo').distinct()

    # Inicializar un diccionario para almacenar gráficos por ciclo
    graphs_curso_por_ciclo = {}

    # Iterar sobre los ciclos y crear gráficos para cada uno
    for ciclo in ciclos:
        ciclo_num = ciclo['ciclo']
        
        # Obtener el número de estudiantes por curso y sección para el ciclo actual
        estudiantes_por_seccion = list(
            MatriculaCurso.objects.filter(seccion__curso__ciclo=ciclo_num)
            .values('seccion__nombre', 'seccion__curso__nombre')
            .annotate(total=Count('matricula'))
        )
        
        # Crear gráfico de estudiantes por sección si hay datos
        if estudiantes_por_seccion:
            # Generar un nuevo campo que combine el curso y la sección
            for item in estudiantes_por_seccion:
                item['curso_seccion'] = f"{item['seccion__curso__nombre']} {item['seccion__nombre']}"
                
            # Crear gráfico usando el nuevo campo 'curso_seccion' para el eje x
            fig_curso = px.bar(
                estudiantes_por_seccion,
                x='curso_seccion',  # Usar la combinación curso y sección
                y='total',
                title=f'Estudiantes por Sección en Ciclo {ciclo_num}',
                labels={'curso_seccion': 'Curso y Sección', 'total': 'Cantidad de Estudiantes'}
            )
            graphs_curso_por_ciclo[ciclo_num] = pio.to_html(fig_curso, full_html=False)

    # Crear gráfico de distribución geográfica
    if distribucion_geografica:
        fig_geografica = px.bar(
            distribucion_geografica,
            x='base',
            y='total',
            title='Distribución Geográfica de Estudiantes Matriculados',
            labels={'base': 'Base', 'total': 'Cantidad de Estudiantes'}
        )
        graph_geografica = pio.to_html(fig_geografica, full_html=False)
    else:
        graph_geografica = None  

    # Paginar los gráficos por ciclo
    page = request.GET.get('page', 1)
    paginator = Paginator(list(graphs_curso_por_ciclo.items()), 3)  # Mostrar 3 gráficos por página
    graphs_curso_paginados = paginator.get_page(page)

    contexto = {
        'total_estudiantes': total_estudiantes,
        'graph_geografica': graph_geografica,
        'graphs_curso_paginados': graphs_curso_paginados,
    }

    return render(request, 'estadisticas/estadisticas_generales.html', contexto)


@login_required
@role_required('Director')
def estadisticas_generales2(request):
    # Total de estudiantes matriculados únicos
    total_estudiantes = Matricula.objects.filter(activa=True).values('estudiante').distinct().count()

    # Distribución geográfica por "base" solo de estudiantes matriculados
    distribucion_geografica = (
        Estudiante.objects
        .filter(id__in=Matricula.objects.filter(activa=True).values('estudiante'))  # Filtra estudiantes matriculados
        .values('base')
        .annotate(total=Count('id'))
    )

    distribucion_geografica = list(distribucion_geografica)

    # Obtener todos los ciclos únicos
    ciclos = Curso.objects.values('ciclo').distinct()

    # Inicializar un diccionario para almacenar gráficos por ciclo
    graphs_curso_por_ciclo = {}

    # Iterar sobre los ciclos y crear gráficos para cada uno
    for ciclo in ciclos:
        ciclo_num = ciclo['ciclo']
        
        # Obtener el número de estudiantes por curso y sección para el ciclo actual
        estudiantes_por_seccion = list(
            MatriculaCurso.objects.filter(seccion__curso__ciclo=ciclo_num)
            .values('seccion__nombre', 'seccion__curso__nombre')
            .annotate(total=Count('matricula'))
        )
        
        # Crear gráfico de estudiantes por sección si hay datos
        if estudiantes_por_seccion:
            # Generar un nuevo campo que combine el curso y la sección
            for item in estudiantes_por_seccion:
                item['curso_seccion'] = f"{item['seccion__curso__nombre']} {item['seccion__nombre']}"
                
            # Crear gráfico usando el nuevo campo 'curso_seccion' para el eje x
            fig_curso = px.bar(
                estudiantes_por_seccion,
                x='curso_seccion',  # Usar la combinación curso y sección
                y='total',
                title=f'Estudiantes por Sección en Ciclo {ciclo_num}',
                labels={'curso_seccion': 'Curso y Sección', 'total': 'Cantidad de Estudiantes'}
            )
            graphs_curso_por_ciclo[ciclo_num] = pio.to_html(fig_curso, full_html=False)

    # Crear gráfico de distribución geográfica
    if distribucion_geografica:
        fig_geografica = px.bar(
            distribucion_geografica,
            x='base',
            y='total',
            title='Distribución Geográfica de Estudiantes Matriculados',
            labels={'base': 'Base', 'total': 'Cantidad de Estudiantes'}
        )
        graph_geografica = pio.to_html(fig_geografica, full_html=False)
    else:
        graph_geografica = None  

    # Paginar los gráficos por ciclo
    page = request.GET.get('page', 1)
    paginator = Paginator(list(graphs_curso_por_ciclo.items()), 3)  # Mostrar 3 gráficos por página
    graphs_curso_paginados = paginator.get_page(page)

    contexto = {
        'total_estudiantes': total_estudiantes,
        'graph_geografica': graph_geografica,
        'graphs_curso_paginados': graphs_curso_paginados,
    }

    return render(request, 'estadisticas/estadisticas_generales2.html', contexto)

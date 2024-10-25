from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from estudiantes.models import Estudiante
from matriculas.models import Matricula, MatriculaCurso
from django.db.models import Count
import plotly.express as px
import plotly.io as pio
from cursos.models import Curso
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template

import base64
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import plotly.io as pio

def estadisticas_generales(request):
    # Total de estudiantes matriculados únicos
    total_estudiantes = Matricula.objects.filter(activa=True).values('estudiante').distinct().count()

    # Distribución geográfica por "base"
    distribucion_geografica = list(Estudiante.objects.values('base').annotate(total=Count('id')))
    
    # Obtener todos los ciclos únicos
    ciclos = Curso.objects.values('ciclo').distinct()

    # Inicializar un diccionario para almacenar gráficos por ciclo
    graphs_curso_por_ciclo = {}

    # Iterar sobre los ciclos y crear gráficos para cada uno
    for ciclo in ciclos:
        ciclo_num = ciclo['ciclo']
        
        # Obtener el número de estudiantes por curso para el ciclo actual
        estudiantes_por_curso = list(
            MatriculaCurso.objects.filter(seccion__curso__ciclo=ciclo_num)
            .values('seccion__curso__nombre')  # Asegúrate de que este campo está disponible
            .annotate(total=Count('matricula'))
        )
        
        # Verifica si estudiantes_por_curso tiene datos
        if estudiantes_por_curso:  # Solo crea gráfico si hay datos
            # Crear gráfico de estudiantes por curso para el ciclo actual
            fig_curso = px.bar(
                estudiantes_por_curso,
                x='seccion__curso__nombre',  # Este campo debe estar presente
                y='total',
                title=f'Estudiantes por Curso - Ciclo {ciclo_num}',
                labels={'seccion__curso__nombre': 'Curso', 'total': 'Cantidad de Estudiantes'}
            )
            graphs_curso_por_ciclo[ciclo_num] = pio.to_html(fig_curso, full_html=False)

    # Crear gráfico de distribución geográfica
    fig_geografica = px.bar(distribucion_geografica, x='base', y='total', title='Distribución Geográfica de Estudiantes', labels={'base': 'Base', 'total': 'Cantidad de Estudiantes'})
    graph_geografica = pio.to_html(fig_geografica, full_html=False)

    contexto = {
        'total_estudiantes': total_estudiantes,
        'graph_geografica': graph_geografica,
        'graphs_curso_por_ciclo': graphs_curso_por_ciclo,  # Gráficos por ciclo
    }

    return render(request, 'estadisticas/estadisticas_generales.html', contexto)
import base64
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import plotly.express as px
import plotly.io as pio

def generar_pdf_estadisticas(request):
    total_estudiantes = Matricula.objects.filter(activa=True).values('estudiante').distinct().count()
    distribucion_geografica = list(Estudiante.objects.values('base').annotate(total=Count('id')))
    ciclos = Curso.objects.values('ciclo').distinct()
    
    graphs_curso_por_ciclo = {}
    
    # Generar gráficos por ciclo
    for ciclo in ciclos:
        ciclo_num = ciclo['ciclo']
        estudiantes_por_curso = list(
            MatriculaCurso.objects.filter(seccion__curso__ciclo=ciclo_num)
            .values('seccion__curso__nombre')
            .annotate(total=Count('matricula'))
        )
        
        if estudiantes_por_curso:
            fig_curso = px.bar(
                estudiantes_por_curso,
                x='seccion__curso__nombre',
                y='total',
                title=f'Estudiantes por Curso - Ciclo {ciclo_num}',
                labels={'seccion__curso__nombre': 'Curso', 'total': 'Cantidad de Estudiantes'}
            )
            # Convertir figura a imagen
            img_curso = pio.to_image(fig_curso, format='png')
            img_curso_b64 = base64.b64encode(img_curso).decode('utf-8')
            graphs_curso_por_ciclo[ciclo_num] = f"data:image/png;base64,{img_curso_b64}"

    # Gráfico de distribución geográfica
    fig_geografica = px.bar(distribucion_geografica, x='base', y='total', title='Distribución Geográfica de Estudiantes', labels={'base': 'Base', 'total': 'Cantidad de Estudiantes'})
    img_geografica = pio.to_image(fig_geografica, format='png')
    img_geografica_b64 = base64.b64encode(img_geografica).decode('utf-8')
    graph_geografica = f"data:image/png;base64,{img_geografica_b64}"

    # Renderizar el template
    contexto = {
        'total_estudiantes': total_estudiantes,
        'graph_geografica': graph_geografica,
        'graphs_curso_por_ciclo': graphs_curso_por_ciclo,
    }
    
    html = render_to_string('estadisticas/estadisticas_generales_pdf.html', contexto)

    # Generar PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="estadisticas_generales.pdf"'
    
    # Convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Comprobar si hubo errores
    if pisa_status.err:
        return HttpResponse('Error generando el PDF')

    return response

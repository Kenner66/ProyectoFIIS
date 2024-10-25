
from django.contrib.auth.decorators import login_required
#from django.contrib.auth import login, logout, authenticate
from usuarios.decorators import role_required 
from cursos.models import HistorialNotas,Curso
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from matriculas.models import Matricula, MatriculaCurso, Seccion, Semestre
from cursos.models import HistorialNotas
from estudiantes.models import Estudiante
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
#from reportlab.lib.pagesizes import letter
#from reportlab.pdfgen import canvas
#from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
#from reportlab.lib import colors
#from reportlab.lib.units import inch
from xhtml2pdf import pisa
#from django.template.loader import render_to_string


@login_required
@role_required('Estudiante')
def cursos_por_ciclo(request):
    # Obtener todos los cursos
    cursos = Curso.objects.all()

    # Agrupar cursos por ciclo
    cursos_por_ciclo = {}
    for curso in cursos:
        if curso.ciclo not in cursos_por_ciclo:
            cursos_por_ciclo[curso.ciclo] = []
        cursos_por_ciclo[curso.ciclo].append(curso)

    # Pasar el diccionario de cursos agrupados al template
    return render(request, 'index/cursos_por_ciclo.html', {
        'cursos_por_ciclo': cursos_por_ciclo,
    })


from django.shortcuts import render, redirect
def verificar_matricula(request):
    if request.user.is_authenticated:
        estudiante = request.user.estudiante
        # Suponiendo que solo hay una matrícula activa
        matricula_activa = Matricula.objects.filter(estudiante=estudiante, estado=True).first()

        if matricula_activa:
            return render(request, 'matricula_activa.html', {'matricula': matricula_activa})
        else:
            return render(request, 'sin_matricula.html')
    else:
        return redirect('home_estudiante')  # O la ruta de inicio de sesión que tengas
        


@login_required
@role_required('Estudiante')
def cargar_secciones_estudiante(request, semestre_id):
    # Asegúrate de que el estudiante está autenticado
    # Filtrar las secciones según el semestre_id
    secciones = Seccion.objects.filter(semestre_id=semestre_id).values('id', 'curso__nombre', 'nombre')
    
    # Retornar las secciones en formato JSON
    return JsonResponse(list(secciones), safe=False)

@login_required
@role_required('Estudiante')
def crear_matricula_estudiante(request):
    # Obtener el estudiante actual
    estudiante = get_object_or_404(Estudiante, usuario=request.user)
    print(estudiante)
    # Obtener semestres activos
    semestres = Semestre.objects.filter(estado=True)

    # Verificar si el estudiante ya está matriculado en un semestre activo
    matricula_existente = Matricula.objects.filter(estudiante=estudiante, semestre__estado=True).exists()

    if matricula_existente:
        # Redirigir a un template que indique que ya está matriculado
        return render(request, 'index/matricula_ya_registrada.html', {
        'estudiante': estudiante,  # Asegúrate de pasar el estudiante aquí
    })

    if request.method == 'GET':
        return render(request, 'index/crear_matricula_estudiante.html', {
            'semestres': semestres,
            'estudiante': estudiante,  # Pasar la información del estudiante al template
        })

    # Si se selecciona un semestre, cargar secciones
    semestre_id = request.GET.get('semestre_id')
    if semestre_id:
        secciones = Seccion.objects.filter(semestre_id=semestre_id)
        secciones_data = [
            {
                'id': seccion.id,
                'nombre_curso': seccion.curso.nombre,
                'seccion': seccion.nombre,
            }
            for seccion in secciones
        ]
        return JsonResponse(secciones_data, safe=False)

    return JsonResponse({'error': 'Semestre no encontrado'}, status=404)


@login_required
@role_required('Estudiante')
def validar_seccion_estudiante(request, seccion_id):
    # Obtener el estudiante basado en el usuario autenticado
    estudiante = get_object_or_404(Estudiante, usuario=request.user)
    # Obtener la sección solicitada
    seccion = get_object_or_404(Seccion, id=seccion_id)
    curso = seccion.curso

    # Validar si el estudiante ya aprobó el curso
    historial = HistorialNotas.objects.filter(estudiante=estudiante, curso=curso).first()
    if historial and historial.nota >= 11:
        return JsonResponse({'error': f'El estudiante ya aprobó el curso {curso.nombre}.'})

    if seccion.cupos_totales <= 0:
        return JsonResponse({'error': f'No hay cupos disponibles para la sección {seccion.nombre} del curso {curso.nombre}.'})
    # Obtener las secciones seleccionadas de la sesión
    secciones_seleccionadas_ids = request.session.get('secciones_seleccionadas', [])
    secciones_seleccionadas = Seccion.objects.filter(id__in=secciones_seleccionadas_ids)

    # Validar prerrequisitos
    prerrequisitos = curso.pre_requisitos.all()
    for prerequisito in prerrequisitos:
        # Comprobar si el estudiante ya ha matriculado el prerrequisito
        matricula_curso = MatriculaCurso.objects.filter(
            matricula__estudiante=estudiante,  # Asegúrate de que Matricula tenga un campo estudiante
            seccion__curso=prerequisito
        ).first()

        # Si no ha matriculado el prerrequisito, verificar si ha aprobado
        if not matricula_curso:
            historial_prerrequisito = HistorialNotas.objects.filter(estudiante=estudiante, curso=prerequisito).first()
            if not (historial_prerrequisito and historial_prerrequisito.nota >= 11):
                return JsonResponse({'error': f'El estudiante no ha aprobado ni seleccionado el prerrequisito {prerequisito.nombre}.'})

    # Validar si el estudiante ya tiene esta sección en su lista de secciones seleccionadas
    if secciones_seleccionadas.filter(id=seccion.id).exists():
        return JsonResponse({'error': f'El estudiante ya ha añadido una sección del curso {curso.nombre}.'})

    # Si todo está bien, devolver una respuesta de éxito
    return JsonResponse({
        'success': 'Validación exitosa, puedes añadir el curso.',
        'curso_nombre': curso.nombre,
        'seccion_nombre': seccion.nombre,
        'creditos': seccion.curso.creditos,
    })

from django.db import transaction

@login_required
@role_required('Estudiante')
def guardar_matricula_estudiante(request):
    if request.method == 'POST':
        # Obtener el estudiante actual a partir del usuario que ha iniciado sesión
        estudiante = get_object_or_404(Estudiante, usuario=request.user)
        
        # Obtener el semestre seleccionado (se espera que sea un único semestre por vez)
        semestre_id = request.POST.get('semestre_id')
        if not semestre_id or not Semestre.objects.filter(id=semestre_id).exists():
            return JsonResponse({'error': 'Semestre no válido.'})

        # Obtener las secciones seleccionadas
        secciones_seleccionadas_ids = request.POST.getlist('secciones_seleccionadas[]')

        # Calcular créditos totales de los cursos seleccionados
        total_creditos = 0
        for seccion_id in secciones_seleccionadas_ids:
            seccion = get_object_or_404(Seccion, id=seccion_id)
            total_creditos += seccion.curso.creditos  # Sumar los créditos de cada curso

        # Validar si los créditos totales exceden el límite
        if total_creditos > 22:
            return JsonResponse({'error': f'No puedes matricular más de 22 créditos. Créditos seleccionados: {total_creditos}.'})

        try:
            # Iniciar una transacción
            with transaction.atomic():
                # Crear o obtener la matrícula para el semestre seleccionado
                matricula, created = Matricula.objects.get_or_create(
                    estudiante=estudiante,
                    semestre_id=semestre_id,
                )

                # Asignar las secciones seleccionadas a la matrícula
                for seccion_id in secciones_seleccionadas_ids:
                    seccion = get_object_or_404(Seccion, id=seccion_id)

                    # Validar que la sección tenga cupos disponibles
                    if seccion.cupos_totales <= 0:
                        return JsonResponse({'error': f'No hay cupos disponibles en la sección {seccion.nombre}.'})

                    # Crear la relación entre la matrícula y la sección si no existe
                    if not MatriculaCurso.objects.filter(matricula=matricula, seccion=seccion).exists():
                        MatriculaCurso.objects.create(matricula=matricula, seccion=seccion)

                        # Disminuir el número de cupos disponibles
                        seccion.cupos_totales -= 1
                        seccion.save()

            return JsonResponse({'success': 'Matrículas guardadas correctamente.'})

        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Método no permitido.'})

@login_required
@role_required('Estudiante')
def descargar_pdf_estudiante(request, estudiante_id):
    # Filtrar las matrículas del estudiante
    matriculas = Matricula.objects.filter(estudiante_id=estudiante_id).prefetch_related('matriculacurso_set')

    # Obtener información del estudiante
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)

    # Calcular créditos por semestre
    creditos_por_semestre = {}
    for matricula in matriculas:
        total_creditos = 0
        cursos = MatriculaCurso.objects.filter(matricula=matricula).prefetch_related('seccion__curso')
        for matricula_curso in cursos:
            total_creditos += matricula_curso.seccion.curso.creditos
        
        creditos_por_semestre[matricula.id] = total_creditos  

    # Crear el objeto HttpResponse con el tipo de contenido adecuado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="matricula_{estudiante_id}.pdf"'

    # Renderizar el HTML desde el template, incluyendo creditos_por_semestre
    html = render_to_string('matriculas/matricula_pdf.html', {
        'matriculas': matriculas,
        'estudiante': estudiante,
        'creditos_por_semestre': creditos_por_semestre
    })

    # Crear el PDF a partir del HTML
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error al generar PDF')

    return response

@login_required
@role_required('Estudiante')
def perfil_estudiante(request):
    estudiante = request.user.estudiante
    informacion_personal = estudiante.informacionpersonal
    return render(request, 'index/perfil.html', {'estudiante': estudiante, 'informacion_personal': informacion_personal})

@login_required
@role_required('Estudiante')
def historial_notas(request):
    historial = HistorialNotas.objects.filter(estudiante=request.user.estudiante)  # Filtra por el estudiante actual
    return render(request, 'index/historial_notas.html', {'historial': historial})
@login_required
@role_required('Estudiante')
def asesorias(request):
    return render(request, 'estudiantes/asesorias.html', {'asesorias': asesorias})


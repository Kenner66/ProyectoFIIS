from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from usuarios.decorators import role_required 
from cursos.models import Curso, HistorialNotas
# Create your views here.
@login_required
@role_required('Estudiante')
def perfil_estudiante(request):
    estudiante = request.user.estudiante
    informacion_personal = estudiante.informacionpersonal
    return render(request, 'index/perfil.html', {'estudiante': estudiante, 'informacion_personal': informacion_personal})
'''
@login_required
@role_required('Estudiante')
def listar_cursos(request):
    cursos = Curso.objects.all()  # Ajusta según tus necesidades
    return render(request, 'estudiantes/cursos.html', {'cursos': cursos})
'''
@login_required
@role_required('Estudiante')
def historial_notas(request):
    historial = HistorialNotas.objects.filter(estudiante=request.user.estudiante)  # Filtra por el estudiante actual
    return render(request, 'index/historial_notas.html', {'historial': historial})
@login_required
@role_required('Estudiante')
def asesorias(request):
    return render(request, 'estudiantes/asesorias.html', {'asesorias': asesorias})

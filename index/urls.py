# urls.py

from django.urls import path
from . import views


urlpatterns = [
    
    path('perfil/', views.perfil_estudiante, name='perfil_estudiante'),
    #path('cursos/', views.listar_cursos, name='listar_cursos'),
    path('historial-notas/', views.historial_notas, name='historial_notas'),
    #path('asesorias/', views.asesorias, name='asesorias'),
    path('cargar_secciones/<int:semestre_id>/', views.cargar_secciones_estudiante, name='cargar_secciones_estudiante'),
    path('guardar_matricula/', views.guardar_matricula_estudiante, name='guardar_matricula_estudiante'),
    path('crear_matricula_estudiante/', views.crear_matricula_estudiante, name='crear_matricula_estudiante'),
    path('validar_seccion/<int:seccion_id>/', views.validar_seccion_estudiante, name='validar_seccion_estudiante'),
    # Otras URLs de tu aplicación
    path('verificar_matricula/', views.verificar_matricula, name='verificar_matricula'),
    path('descargar_pdf/<int:estudiante_id>/', views.descargar_pdf_estudiante, name='descargar_pdf_estudiante'), # Asegúrate de tener la importación correcta
    path('cursos_por_ciclo/', views.cursos_por_ciclo, name='cursos_por_ciclo'),

]



from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_cursos, name='listar_cursos'),
    path('agregar/', views.agregar_curso, name='agregar_curso'),
    path('editar/<int:pk>/', views.editar_curso, name='editar_curso'),
    path('historial/', views.listar_estudiantes_historial, name='listar_estudiantes_historial'),
    path('historial/<int:estudiante_id>/', views.historial_notas_estudiante, name='historial_notas_estudiante'),
    path('historial/<int:estudiante_id>/agregar_nota/', views.agregar_nota, name='agregar_nota'),
    path('cargar-cursos-csv/', views.cargar_cursos_csv, name='cargar_cursos_csv'),
]


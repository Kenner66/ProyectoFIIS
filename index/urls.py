# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.perfil_estudiante, name='perfil_estudiante'),
    #path('cursos/', views.listar_cursos, name='listar_cursos'),
    path('historial-notas/', views.historial_notas, name='historial_notas'),
    path('asesorias/', views.asesorias, name='asesorias'),
    #path('horarios/', views.horarios, name='horarios'),
]

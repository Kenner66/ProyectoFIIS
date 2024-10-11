from django.urls import path
from . import views
from .views import (
    listar_matriculas,
    crear_matricula,
    cargar_secciones,
    validar_seccion,
)

urlpatterns = [
    path('matriculas/', listar_matriculas, name='listar_matriculas'),
    path('matriculas/crear/', crear_matricula, name='crear_matricula'),
    path('matriculas/cargar_secciones/<int:semestre_id>/', cargar_secciones, name='cargar_secciones'),
    #path('matriculas/validar_seccion/<str:codigo_estudiante>/<int:seccion_id>/', validar_seccion, name='validar_seccion'),
    path('cargar_secciones/<int:semestre_id>/', views.cargar_secciones, name='cargar_secciones'),
    path('validar_seccion/<str:codigo_estudiante>/<int:seccion_id>/', views.validar_seccion, name='validar_seccion'),
    #path('matriculas/remover_seccion/<str:codigo_estudiante>/<int:seccion_id>/', remover_seccion, name='remover_seccion'),
]


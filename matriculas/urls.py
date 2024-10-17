
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
    path('guardar_matricula/', views.guardar_matricula, name='guardar_matricula'),
    path('eliminar_matricula/<int:matricula_id>/', views.eliminar_matricula, name='eliminar_matricula'),
    path('ver_matricula/<int:matricula_id>/', views.ver_matricula, name='ver_matricula'),
    path('matriculas/pdf/<int:estudiante_id>/',views.descargar_pdf, name='descargar_pdf'),
    #path('matriculas/remover_seccion/<str:codigo_estudiante>/<int:seccion_id>/', remover_seccion, name='remover_seccion'),
]


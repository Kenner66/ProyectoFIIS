from django.urls import path
from . import views

urlpatterns = [
    path('estudiantes/', views.listar_estudiantes, name='listar_estudiantes'),
    path('estudiantes/agregar/', views.agregar_estudiante, name='agregar_estudiante'),
    path('estudiantes/editar/<int:pk>/', views.editar_estudiante, name='editar_estudiante'),
]

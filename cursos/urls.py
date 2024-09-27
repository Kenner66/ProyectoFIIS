from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_cursos, name='listar_cursos'),
    path('agregar/', views.agregar_curso, name='agregar_curso'),
    path('editar/<int:pk>/', views.editar_curso, name='editar_curso'),
]
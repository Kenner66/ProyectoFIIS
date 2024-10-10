from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_semestres, name='listar_semestres'),
    path('agregar/', views.agregar_semestre, name='agregar_semestre'),
    path('editar/<int:semestre_id>/', views.editar_semestre, name='editar_semestre'),
]

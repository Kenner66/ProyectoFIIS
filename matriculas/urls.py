from django.urls import path
from .import views   # Asegúrate de importar la vista listar_matriculas

urlpatterns = [
    # Otras URLs
    path('matricular/', views.matricular_estudiante, name='matricular_estudiante'),
    path('', views.listar_matriculas, name='listar_matriculas'),  # Asegúrate de tener esta vista
    path('editar/<int:matricula_id>/', views.editar_matricula, name='editar_matricula'),
]

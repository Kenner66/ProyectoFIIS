from django.urls import path
from .import views
urlpatterns = [
    path('', views.listar_profesores, name='listar_profesores'),
    path('agregar/', views.agregar_profesor, name='agregar_profesor'),
    path('editar/<int:profesor_id>/', views.editar_profesor, name='editar_profesor'),
]

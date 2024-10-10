
from django.urls import path
from . import views
urlpatterns = [
    path('', views.listar_horarios, name='listar_horarios'),
    path('agregar/', views.agregar_horario, name='agregar_horario'),
    path('editar_horario/<int:horario_id>/', views.editar_horario, name='editar_horario'),
    path('secciones/', views.listar_secciones, name='listar_secciones'),
    path('secciones/agregar/', views.agregar_seccion, name='agregar_seccion'),
    path('secciones/editar/<int:seccion_id>/', views.editar_seccion, name='editar_seccion'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_estudiantes, name='listar_estudiantes'),
    path('agregar/', views.agregar_estudiante, name='agregar_estudiante'),
    path('editar/<int:pk>/', views.editar_estudiante, name='editar_estudiante'),
    path('<int:pk>/ver/', views.ver_informacion_estudiante, name='ver_informacion_estudiante'),
    path('agregar_informacion/<int:estudiante_id>/', views.agregar_informacion_personal, name='agregar_informacion_personal'),
    path('<int:pk>/editar_informacion/', views.editar_informacion_personal, name='editar_informacion_personal'),
    path('cargar-estudiantes-csv/', views.cargar_estudiantes_csv, name='cargar_estudiantes_csv'),
]

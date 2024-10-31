from django.urls import path
from . import views

urlpatterns = [
    path('estadisticas/', views.estadisticas_generales, name='estadisticas_generales'),
    path('estadisticas2/', views.estadisticas_generales2, name='estadisticas_generales2'),
]

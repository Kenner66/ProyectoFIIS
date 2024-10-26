from django.urls import path
from . import views

urlpatterns = [
    path('estadisticas/', views.estadisticas_generales, name='estadisticas_generales'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('estadisticas/', views.estadisticas_generales, name='estadisticas_generales'),
    path('generar_pdf_estadisticas/', views.generar_pdf_estadisticas, name='generar_pdf_estadisticas'),
]

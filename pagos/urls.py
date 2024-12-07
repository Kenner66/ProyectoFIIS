from django.urls import path
from . import views

urlpatterns = [
    path('crear-preferencia/', views.crear_preferencia, name='crear_preferencia'),
]
    
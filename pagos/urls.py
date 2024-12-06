from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_preferencia, name='crear_preferencia'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
    path('pending/', views.pending, name='pending'),
]
    
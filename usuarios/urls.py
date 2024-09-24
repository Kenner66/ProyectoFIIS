from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('home/', views.home, name='home'),
    path('signout/', views.signout, name='signout'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('home-admin/', views.home_admin, name='home_admin'),
    path('home-estudiante/', views.home_estudiante, name='home_estudiante'),
]
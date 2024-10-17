from django.urls import path
from . import views

from django.contrib.auth.views import PasswordResetConfirmView
from .views import CustomPasswordResetView 
from django.views.generic import TemplateView
urlpatterns = [
    path('', views.signin, name='signin'),
    #path('home/', views.home, name='home'),
    path('signout/', views.signout, name='signout'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('home-admin/', views.home_admin, name='home_admin'),
    path('home-estudiante/', views.home_estudiante, name='home_estudiante'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', TemplateView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),  # Página de éxito
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Vista para confirmar el restablecimiento
    path('reset/done/', TemplateView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('cargar-usuarios-csv/', views.cargar_usuarios_csv, name='cargar_usuarios_csv'),
]   
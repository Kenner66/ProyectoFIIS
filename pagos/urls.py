from django.urls import path
from . import views

urlpatterns = [
    #path("verificar-pago/", views.verificar_pago_view, name="verificar_pago"),
    path('pagos/', views.lista_pagos_admin, name='lista_pagos'),
    path('validar-pago/', views.validar_pago_alumno, name='validar_pago_alumno'),
]
    
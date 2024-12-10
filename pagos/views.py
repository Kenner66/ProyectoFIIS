import mercadopago
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
import mercadopago
from django.http import JsonResponse
from .forms import VerificarPagoForm
from .utils import verificar_pago,registrar_pagos,obtener_pagos_realizados  
from .models import Pago

import mercadopago
from datetime import datetime, timedelta
from django.conf import settings

'''
def verificar_pago_view(request):
    mensaje = None
    estado = None

    if request.method == "POST":
        form = VerificarPagoForm(request.POST)
        if form.is_valid():
            numero_operacion = form.cleaned_data["numero_operacion"]
            resultado = verificar_pago(numero_operacion)

            if "error" not in resultado and resultado["status"] == "approved":
                registrar_pago(resultado)  # Llama al registro aquí
                mensaje = f"El pago con número de operación {numero_operacion} está aprobado y registrado."
                estado = "success"
            else:
                mensaje = f"No se pudo verificar el pago con número de operación {numero_operacion}."
                estado = "error"
    else:
        form = VerificarPagoForm()

    return render(request, "pagos/verificar_pago.html", {"form": form, "mensaje": mensaje, "estado": estado})

'''
def lista_pagos_admin(request):
    pagos = obtener_pagos_realizados()
    pagos = Pago.objects.all()

    return render(request, "pagos/lista_pagos.html", {"pagos": pagos})
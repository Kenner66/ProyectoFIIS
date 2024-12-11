
import mercadopago
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
import mercadopago
from .utils import registrar_pagos,obtener_pagos_realizados  
from .models import Pago
from .models import Pago, ValidacionPago
from estudiantes.models import Estudiante
import mercadopago
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Pago, ValidacionPago    
from django.contrib.auth.decorators import login_required
from usuarios.decorators import role_required

@login_required
@role_required('Estudiante')
def validar_pago_alumno(request):
    if request.method == "POST":
        numero_operacion = request.POST.get('numero_operacion')
        estudiante = Estudiante.objects.filter(usuario=request.user).first()

        if not estudiante:
            messages.error(request, "No se encontró un perfil de estudiante asociado a tu cuenta.")
            return redirect('validar_pago_alumno')

        # Buscar el pago
        pago = Pago.objects.filter(numero_operacion=numero_operacion, estado="approved").first()

        if not pago:
            messages.error(request, "El número de operación no es válido o el pago no está aprobado.")
            return redirect('validar_pago_alumno')

        # Verificar si el pago ya está asociado
        if ValidacionPago.objects.filter(pago=pago).exists():
            messages.error(request, "Este número de operación ya está asociado a otro estudiante.")
            return redirect('validar_pago_alumno')

        # Verificar si el estudiante ya tiene un pago asociado
        if ValidacionPago.objects.filter(estudiante=estudiante).exists():
            messages.error(request, "Ya tienes un pago validado. No puedes validar otro.")
            return redirect('validar_pago_alumno')

        # Asociar el pago al estudiante
        ValidacionPago.objects.create(estudiante=estudiante, pago=pago)
        messages.success(request, "Pago validado con éxito. Puedes proceder con tu matrícula.")
        return redirect('crear_matricula_estudiante')  # Redirige al template de matrícula

    return render(request, 'pagos/validar_pago_alumno.html')

@login_required
@role_required('Administrador')
def lista_pagos_admin(request):
    pagos = obtener_pagos_realizados()
    pagos = Pago.objects.all()

    return render(request, "pagos/lista_pagos.html", {"pagos": pagos})
    
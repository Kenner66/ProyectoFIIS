import mercadopago
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse

def crear_preferencia(request):
    # Inicializa Mercado Pago SDK con el Access Token
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    # Crear la preferencia de pago
    preferencia = {
        "items": [
            {
                "title": "Matrícula Universitaria",  # Nombre del producto
                "quantity": 1,  # Cantidad
                "unit_price": 65.0,  # Precio del producto
            }
        ],
        "back_urls": {
            "success": "https://matricula-4nrt.onrender.com//pagos/success",  # URL de éxito
            "failure": "https://matricula-4nrt.onrender.com//pagos/failure",  # URL de fracaso
            "pending": "https://matricula-4nrt.onrender.com//pagos/pending",  # URL de pendiente
        },
        "auto_return": "approved",  # Redirigir automáticamente a la página de éxito si el pago es aprobado
    }

    # Crear la preferencia con la API de Mercado Pago
    response = sdk.preference().create(preferencia)

    if response['status'] == 201:
        # Obtener el link para redirigir al usuario
        init_point = response['response']['init_point']
        return redirect(init_point)  # Redirige al usuario al punto de inicio de pago
    else:
        # Si ocurre un error, puedes mostrar un mensaje
        return HttpResponse(f"Error: {response['response']['message']}", status=500)



def success(request):
    return HttpResponse("¡Pago exitoso!")

def failure(request):
    return HttpResponse("El pago no fue aprobado.")

def pending(request):
    return HttpResponse("El pago está pendiente.")

import mercadopago
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
import mercadopago

def crear_preferencia(request):
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    preferencia = {
        "items": [
            {
                "title": "Pago de matrícula",
                "quantity": 1,
                "unit_price": 1,
                "currency_id": "PEN",
            }
        ],
        "back_urls": {
            "success": "https://matricula-4nrt.onrender.com/success",
            "failure": "https://matricula-4nrt.onrender.com/failure",
            "pending": "https://matricula-4nrt.onrender.com/pending"
        },
        "auto_return": "approved",
    }
    respuesta = sdk.preference().create(preferencia)
    init_point = respuesta["response"]["init_point"]
    return redirect(init_point)


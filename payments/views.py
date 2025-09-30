from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests, hmac, hashlib

# Página principal
def index(request):
    return render(request, 'payments/index.html')

# Crear el pago
def create_payment(request):
    url = "https://api.commerce.coinbase.com/charges"

    payload = {
        "name": "Test Payment",
        "description": "Pago de prueba con Coinbase",
        "pricing_type": "fixed_price",
        "local_price": {
            "amount": "0.01",
            "currency": "USD"
        },
        "metadata": {
            "order_id": "test123"
        }
        # OJO: quitamos redirect_url y cancel_url, no son necesarios
    }

    headers = {
        "X-CC-Api-Key": settings.COINBASE_API_KEY,
        "X-CC-Version": "2018-03-22",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    if "data" in data and "hosted_url" in data["data"]:
        # Coinbase muestra directamente el recibo en hosted_url
        return JsonResponse({"url": data["data"]["hosted_url"]})
    else:
        return JsonResponse(data,status=400)

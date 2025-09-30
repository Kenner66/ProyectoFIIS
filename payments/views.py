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
        },
        "redirect_url": request.build_absolute_uri('/payments/success'),
        "cancel_url": request.build_absolute_uri('/payments/cancel')
    }

    headers = {
        "X-CC-Api-Key": settings.COINBASE_API_KEY,
        "X-CC-Version": "2018-03-22",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if "data" in data and "hosted_url" in data["data"]:
        return JsonResponse({"url": data["data"]["hosted_url"]})
    else:
        return JsonResponse(data, status=400)

# Éxito y cancelación
def success(request):
    return render(request, 'payments/success.html')

def cancel(request):
    return render(request, 'payments/cancel.html')

# Webhook Coinbase
@csrf_exempt  # Coinbase no envía CSRF token
def webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")

    raw_body = request.body
    signature = request.headers.get("X-CC-Webhook-Signature", "")

    secret = settings.COINBASE_WEBHOOK_SHARED_SECRET
    if secret:
        computed = hmac.new(
            secret.encode(),
            raw_body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(computed, signature):
            return HttpResponseBadRequest("Firma inválida")

    event = request.json if hasattr(request, "json") else None
    print("Webhook recibido:", event)
    return HttpResponse(status=200)

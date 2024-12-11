import mercadopago
from django.conf import settings
from .models import Pago
from datetime import datetime, timedelta    

def obtener_pagos_realizados():
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=30)  # Últimos 30 días
    
    filtros = {
        "range": "date_created",
        "begin_date": fecha_inicio.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end_date": fecha_fin.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "approved",  # Solo pagos aprobados
        "sort": "date_created",
        "criteria": "desc",  # Ordenar de más reciente a más antiguo
    }

    respuesta = sdk.payment().search(filters=filtros)
    
    if respuesta["status"] == 200:
        pagos = respuesta["response"]["results"]
        registrar_pagos(pagos)  # Registrar los pagos en la base de datos
        return pagos
    else:
        return []

def registrar_pagos(pagos):
    for pago in pagos:
        # Verifica si el pago ya está registrado en la base de datos
        if not Pago.objects.filter(numero_operacion=pago["id"]).exists():
            nuevo_pago = Pago(
                numero_operacion=pago["id"],
                estado=pago["status"],
                monto=pago["transaction_amount"],
                comprador_email=pago["payer"]["email"],
                fecha_pago=pago["date_created"],
                metodo_pago=pago.get("payment_method_id", "No especificado"),
                tarjeta_ultimos_digitos=pago.get("card", {}).get("last_four_digits", ""),
            )
            nuevo_pago.save()

import json
import os
from ..models import Tickets
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

def qr_scanner(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        qr_code_data = data.get('qr_code_data')
        try:
            ticket = Tickets.objects.get(barcode=qr_code_data)
        except Tickets.DoesNotExist:
            return JsonResponse({
            'error' : 'Ticket Doesnt Exist'}, status=404)

        path = os.path.join(settings.BASE_DIR, 'manage_barcode', 'static', "barcodes", f"{ticket.client.email}.png")
        if os.path.exists(path):
            os.remove(path)
            ticket.delete()
            return JsonResponse({
                'success' : 'Ticket used'
            }, status=200)
        else:
            return JsonResponse({
            'error' : 'Ticket Doesnt Exist'}, status=404)

    return JsonResponse({
            'error' : 'Method Not Allowed'
        }, status=405)


def scanner(request):
    return render(request, 'pages/scanner.html')
from django.shortcuts import render
from django.http import JsonResponse
from .models import FormData

def submit_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        FormData.objects.create(name=name, email=email)
        return JsonResponse({'message': 'Data saved successfully'})
    return render(request, 'index.html')

def index(request):
    return render(request, 'index.html')
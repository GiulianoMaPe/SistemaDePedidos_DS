from django.http import JsonResponse

def api_home(request):
    return JsonResponse({"mensaje": "Bienvenido a la API de Cocos Burguer"})
from django.shortcuts import render

# Create your views here.

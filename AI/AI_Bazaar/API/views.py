from django.shortcuts import render
from django.http import JsonResponse
from django.urls import path
from .views import hello_api

# Create your views here.

def hello_api(request):
    data = {
        "message": "Merhaba, AI_Bazaar API çalışıyor!"
    }
    return JsonResponse(data)

urlpatterns = [
    path('hello/', hello_api),
]
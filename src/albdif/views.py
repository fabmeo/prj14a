from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def proprieta_detail(request, proprieta_id):
    return HttpResponse("Dettaglio della proprietà %s." % proprieta_id)


def camera_detail(request, camera_id):
    response = "Questa è la camera %s."
    return HttpResponse(response % camera_id)

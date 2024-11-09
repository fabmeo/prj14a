from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader

from .models import Stagione, Camera, Proprieta, Prenotazione


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# PROPRIETA'
def proprieta_detail(request, proprieta_id):
    response = "Questa è la proprieta %s."
    return HttpResponse(response % proprieta_id)


def proprieta_list(request):
    w_proprieta_list = Proprieta.objects.order_by("descrizione")[:5]
    context = {"proprieta_list": w_proprieta_list}
    return render(request, "albdif/proprieta_list.html", context)


# CAMERE
def camera_detail(request, camera_id):
    response = "Questa è la camera %s."
    return HttpResponse(response % camera_id)


def camere_list(request):
    w_camere_list = Camera.objects.order_by("descrizione")[:5]
    context = {"camere_list": w_camere_list}
    return render(request, "albdif/camere_list.html", context)


# STAGIONI
def stagione_detail(request, stagione_id):
    s = get_object_or_404(Stagione, pk=stagione_id)
    return render(request, "albdif/stagione_detail.html", {"stagione": s})


def stagioni_list(request):
    w_stagioni_list = Stagione.objects.order_by("-data_inizio")[:5]
    context = {"stagioni_list": w_stagioni_list}
    return render(request, "albdif/stagioni_list.html", context)


# PRENOTAZIONI
def prenotazione_detail(request, prenotazione_id):
    s = get_object_or_404(Prenotazione, pk=prenotazione_id)
    return render(request, "albdif/prenotazione_detail.html", {"prenotazione": s})


def prenotazioni_list(request):
    w_prenotazioni_list = Prenotazione.objects.order_by("-data_prenotazione")[:5]
    context = {"prenotazioni_list": w_prenotazioni_list}
    return render(request, "albdif/prenotazioni_list.html", context)

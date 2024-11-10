from datetime import datetime
from threading import get_ident

from django.core.servers.basehttp import get_internal_wsgi_application
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils.dateformat import format
import json

from .models import Stagione, Camera, Proprieta, Prenotazione, PrezzoCamera, CalendarioPrenotazione
from .utils import date_range


def home(request):
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
    camera = get_object_or_404(Camera, pk=camera_id)

    gia_prenotate = []
    prenotazioni = Prenotazione.objects.filter(camera=camera_id)
    for p in prenotazioni:
        # estraggo solo i periodi che comprendono la data corrente e i futuri
        periodi = CalendarioPrenotazione.objects.filter(prenotazione=p.id, data_fine__gte=datetime.today())
        for periodo in periodi:
            for d in date_range(str(periodo.data_inizio), str(periodo.data_fine)):
                gia_prenotate.append(d)

    context = {"camera": camera, 'disabled_dates': json.dumps(gia_prenotate)}
    return render(request, "albdif/camera_detail.html", context)


def camere_list(request):
    w_camere_list = Camera.objects.order_by("descrizione")[:5]
    context = {"camere_list": w_camere_list}
    return render(request, "albdif/camere_list.html", context)


def prezzo_camera_detail(request, prezzocamera_id):
    response = "Questa è il prezzo della camera %s."
    return HttpResponse(response % prezzocamera_id)


def prezzi_camera_list(request):
    w_prezzi_camera_list = PrezzoCamera.objects.order_by("camera")
    context = {"prezzi_camera_list": w_prezzi_camera_list}
    return render(request, "albdif/prezzi_camera_list.html", context)


# STAGIONI
class stagione_detail(generic.DetailView):
    model = Stagione
    template_name = "albdif/stagione_detail.html"


class stagioni_list(generic.ListView):
    template_name = "albdif/stagioni_list.html"
    context_object_name = "stagioni_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Stagione.objects.order_by("-data_inizio")[:5]

# def stagione_detail(request, stagione_id):
#     s = get_object_or_404(Stagione, pk=stagione_id)
#     return render(request, "albdif/stagione_detail.html", {"stagione": s})
#
#
# def stagioni_list(request):
#     w_stagioni_list = Stagione.objects.order_by("-data_inizio")[:5]
#     context = {"stagioni_list": w_stagioni_list}
#     return render(request, "albdif/stagioni_list.html", context)


# PRENOTAZIONI
def prenotazione_detail(request, prenotazione_id):
    s = get_object_or_404(Prenotazione, pk=prenotazione_id)
    return render(request, "albdif/prenotazione_detail.html", {"prenotazione": s})


def prenotazioni_list(request):
    w_prenotazioni_list = Prenotazione.objects.order_by("-data_prenotazione")[:5]
    context = {"prenotazioni_list": w_prenotazioni_list}
    return render(request, "albdif/prenotazioni_list.html", context)


def calendario_prenotazione_detail(request, calendario_prenotazione_id):
    s = get_object_or_404(CalendarioPrenotazione, pk=calendario_prenotazione_id)
    return render(request, "albdif/calendario_prenotazione_detail.html", {"calendario_prenotazione": s})


def calendario_prenotazioni_list(request):
    w_calendario_prenotazioni_list = CalendarioPrenotazione.objects.order_by("data_inizio")
    context = {"calendario_prenotazioni_list": w_calendario_prenotazioni_list}
    return render(request, "albdif/calendario_prenotazioni_list.html", context)


def calendario_camera(request, camera_id=None):
    # Lista delle date già prenotate (formato "yyyy-mm-dd")
    gia_prenotate = [
        '2024-12-10',
        '2024-12-15',
        '2024-12-20'
    ]
    gia_prenotate = Camera.objects.filter(pk=camera_id).values_list('data_prenotazione', flat=True)
    context = {
        'disabled_dates': json.dumps(gia_prenotate)
    }
    return render(request, "albdif/calendario_camera.html", context)

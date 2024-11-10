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


# PROPRIETA'
class proprieta_detail(generic.DetailView):
    model = Proprieta
    template_name = "albdif/proprieta_detail.html"


class proprieta_list(generic.ListView):
    template_name = "albdif/proprieta_list.html"
    context_object_name = "proprieta_list"

    def get_queryset(self):
        """Ritorna le prime 5 proprietà presenti"""
        return Proprieta.objects.order_by("descrizione")[:5]


# CAMERE
class camera_detail(generic.DetailView):
    model = Camera
    template_name = "albdif/camera_detail.html"

    def get_context_data(self, **kwargs):
        context = super(camera_detail, self).get_context_data(**kwargs)

        gia_prenotate = []
        prenotazioni = Prenotazione.objects.filter(camera=self.object.pk)
        for p in prenotazioni:
            # estraggo solo i periodi che comprendono la data corrente e i futuri
            periodi = CalendarioPrenotazione.objects.filter(prenotazione=p.id, data_fine__gte=datetime.today())
            for periodo in periodi:
                for d in date_range(str(periodo.data_inizio), str(periodo.data_fine)):
                    gia_prenotate.append(d)

        context['disabled_dates'] = json.dumps(gia_prenotate)
        return context


class camere_list(generic.ListView):
    template_name = "albdif/camere_list.html"
    context_object_name = "camere_list"

    def get_queryset(self):
        """Ritorna la lista delle camere ordinata per descrizione"""
        return Camera.objects.order_by("descrizione")


class prezzo_camera_detail(generic.DetailView):
    model = PrezzoCamera
    template_name = "albdif/prezzo_camera_detail.html"


class prezzi_camera_list(generic.ListView):
    template_name = "albdif/prezzi_camera_list.html"
    context_object_name = "prezzi_camera_list"

    def get_queryset(self):
        """Ritorna la lista delle camere ordinata per descrizione"""
        return PrezzoCamera.objects.order_by("camera")


# PRENOTAZIONI
class prenotazione_detail(generic.DetailView):
    model = Prenotazione
    template_name = "albdif/prenotazione_detail.html"

    def get_context_data(self, **kwargs):
        context = super(prenotazione_detail, self).get_context_data(**kwargs)

        gia_prenotate = []
        # estraggo solo i periodi che comprendono la data corrente e i futuri
        periodi = CalendarioPrenotazione.objects.filter(prenotazione=self.object.pk, data_fine__gte=datetime.today())
        for periodo in periodi:
            for d in date_range(str(periodo.data_inizio), str(periodo.data_fine)):
                gia_prenotate.append(d)

        context['disabled_dates'] = json.dumps(gia_prenotate)
        return context


class prenotazioni_list(generic.ListView):
    template_name = "albdif/prenotazioni_list.html"
    context_object_name = "prenotazioni_list"

    def get_queryset(self):
        """Ritorna la lista delle prenotazioni ordinata per data più reente"""
        return Prenotazione.objects.order_by("-data_prenotazione")


class calendario_prenotazione_detail(generic.DetailView):
    model = CalendarioPrenotazione
    template_name = "albdif/calendario_prenotazione_detail.html"


class calendario_prenotazioni_list(generic.ListView):
    template_name = "albdif/calendario_prenotazioni_list.html"
    context_object_name = "calendario_prenotazioni_list"

    def get_queryset(self):
        """Ritorna la lista delle date di prenotazione ordinata per data"""
        return CalendarioPrenotazione.objects.order_by("data_inizio")


def calendario_camera(request, camera_id=None):
    # Lista delle date già prenotate di una camera (formato "yyyy-mm-dd")
    gia_prenotate = Camera.objects.filter(pk=camera_id).values_list('data_prenotazione', flat=True)
    # @TODO Estrai le date del calendario_prenotazione
    context = {
        'disabled_dates': json.dumps(gia_prenotate)
    }
    return render(request, "albdif/calendario_camera.html", context)



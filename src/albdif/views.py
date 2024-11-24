from datetime import datetime
from .utils import date_range

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.views import generic
import json

from .models import Camera, Proprieta, Prenotazione, PrezzoCamera, CalendarioPrenotazione, Foto


def home(request: HttpRequest) -> HttpResponse:
    template_name = "albdif/home.html"
    return render(request, template_name)


# PROPRIETA'
class proprieta_detail(generic.ListView):
    """
    Ritorna la lista delle camere dell'AD selezionato ordinata per descrizione
    """
    template_name = "albdif/proprieta_detail.html"
    context_object_name = "camere_list"

    def get_queryset(self):
        prop = self.kwargs.get('pk')
        return Camera.objects.filter(proprieta__id=prop).order_by("descrizione")

    def get_context_data(self, **kwargs):
        context = super(proprieta_detail, self).get_context_data(**kwargs)
        prop = get_object_or_404(Proprieta, pk=self.kwargs.get('pk'))
        context['proprieta'] = prop                  # la proprietà (Albergo Diffuso X)
        context['camere_list'] = self.get_queryset() # le sue camere
        return context


class proprieta_partner(generic.ListView):
    """
    Ritorna la lista dei partner con le foto della proprietà
    """
    template_name = "albdif/proprieta_list.html"
    context_object_name = "proprieta_list"

    def get_queryset(self):
        return Proprieta.objects.filter(principale=False)

    def get_context_data(self, **kwargs):
        context = super(proprieta_partner, self).get_context_data(**kwargs)
        prop_e_foto = []
        for p in self.get_queryset():
            prop = {'prop': p, 'foto': Foto.objects.filter(proprieta__id=p.id)}
            prop_e_foto.append(prop)
        context['prop_e_foto'] = prop_e_foto      # ogni proprietà con le sue foto
        return context


# CAMERE
class camera_detail(generic.DetailView):
    """
    # estraggo solo i periodi di prenotazione che comprendono la data corrente e i futuri
    """
    model = Camera
    template_name = "albdif/camera_detail.html"

    def get_context_data(self, **kwargs):
        context = super(camera_detail, self).get_context_data(**kwargs)
        gia_prenotate = []
        prenotazioni = Prenotazione.objects.filter(camera=self.object.pk)
        for p in prenotazioni:
            periodi = CalendarioPrenotazione.objects.filter(prenotazione=p.id, data_fine__gte=datetime.today())
            for periodo in periodi:
                for d in date_range(str(periodo.data_inizio), str(periodo.data_fine)):
                    gia_prenotate.append(d)

        foto = Foto.objects.filter(camera=self.object.pk)
        context['disabled_dates'] = json.dumps(gia_prenotate)
        context['foto'] = foto
        return context


class camere_list(generic.ListView):
    """
    Ritorna la lista delle camere dell'AD principale ordinata per descrizione
    """
    template_name = "albdif/camere_list.html"
    context_object_name = "camere_list"

    def get_queryset(self):
        return Camera.objects.filter(proprieta__principale=True).order_by("descrizione")


class prezzo_camera_detail(generic.DetailView):
    model = PrezzoCamera
    template_name = "albdif/prezzo_camera_detail.html"


class prezzi_camera_list(generic.ListView):
    """
    Ritorna la lista dei prezzi di una camera
    @TODO modificare per accettare parametro ed elencare solo i prezzi di  una camera
    """
    template_name = "albdif/prezzi_camera_list.html"
    context_object_name = "prezzi_camera_list"

    def get_queryset(self):
        return PrezzoCamera.objects.order_by("camera.descrizione")


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


class prenotazioni_utente_list(generic.ListView):
    template_name = "albdif/prenotazioni_list.html"
    context_object_name = "prenotazioni_list"

    def get_queryset(self):
        """Ritorna la lista delle prenotazioni di un utente"""
        utente_id = self.kwargs.get('pk')
        return Prenotazione.objects.filter(visitatore=utente_id).order_by("-data_prenotazione")

    def get_context_data(self, **kwargs):
        context = super(prenotazioni_utente_list, self).get_context_data(**kwargs)
        return context


class calendario_prenotazione_detail(generic.DetailView):
    model = CalendarioPrenotazione
    template_name = "albdif/calendario_prenotazione_detail.html"


class calendario_prenotazioni_list(generic.ListView):
    template_name = "albdif/calendario_prenotazioni_list.html"
    context_object_name = "calendario_prenotazioni_list"

    def get_queryset(self):
        """Ritorna la lista delle date di prenotazione ordinata per data"""
        return CalendarioPrenotazione.objects.order_by("data_inizio")


# def calendario_camera(request, camera_id=None):
#     # Lista delle date già prenotate di una camera (formato "yyyy-mm-dd")
#     gia_prenotate = Camera.objects.filter(pk=camera_id).values_list('data_prenotazione', flat=True)
#     # @TODO Estrai le date del calendario_prenotazione
#     context = {
#         'disabled_dates': json.dumps(gia_prenotate)
#     }
#     return render(request, "albdif/calendario_camera.html", context)



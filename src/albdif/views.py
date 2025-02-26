from datetime import datetime, date
import json
from lib2to3.fixes.fix_input import context
from venv import logger

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.contrib.auth import authenticate, login as auth_login
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.views import generic
from django.contrib.auth import logout as auth_logout
from django.db import transaction
from django.db.models import F, Q

from .config import settings
from .forms import LoginForm, PrenotazioneForm, CalendarioPrenotazioneForm, PagamentoForm, RegistrazioneForm, \
    RegistrazioneTitolareForm
from .utils.utility import date_range, calcola_prezzo_totale, to_date
from .models import Camera, Proprieta, Prenotazione, PrezzoCamera, CalendarioPrenotazione, Foto, Visitatore, Stagione, \
    ServizioCamera, RuoloUtente, RichiestaAdesione


def home(request: HttpRequest) -> HttpResponse:
    """
    Gestisce la home del sito
    """
    template_name = "albdif/home.html"
    return render(request, template_name)


class login(FormView):
    """
    Gestisce la pagina che effettua il login
    """
    template_name = "albdif/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('albdif:home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())

        form.add_error(None, "Username o password errate!")
        return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        github_sso = google_sso = False
        if hasattr(settings, "SOCIAL_AUTH_GITHUB_KEY") and settings.SOCIAL_AUTH_GITHUB_KEY > "":
            github_sso = True
        if hasattr(settings, "GOOGLE_CLIENT_ID") and settings.GOOGLE_CLIENT_ID:
            google_sso = True
        context = {"github_sso": github_sso, "google_sso": google_sso}
        return render(request, self.template_name, context)


class logout(View):
    """
    Esegue il logout dell'utente e ritorna ad home
    """
    def post(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('albdif:home')


# REGISTRAZIONE
class registrazione(generic.DetailView):
    """
    # Gestisce la pagina di registrazione dell'utente Visitatore
    """
    template_name = "albdif/form_registrazione.html"

    def get(self, request, *args, **kwargs):

        registrazione_form = RegistrazioneForm()
        return render(request, self.template_name, {
            'form': registrazione_form,
        })

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            registrazione_form = RegistrazioneForm(request.POST)
            if registrazione_form.is_valid():
                user_data = registrazione_form.cleaned_data
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    #first_name=user_data['first_name'],
                    #last_name=user_data['last_name']
                )
                # crea il visitatore legandolo all'utente appena registrato
                v = Visitatore.objects.create(utente=user, registrazione=datetime.now())
                # salva l'istanza
                v.save()
                # preleva il gruppo/ruolo dell'utente
                gruppo = Group.objects.filter(name="Visitatore").first()
                # crea il ruolo dell'utente sul sito (i visitatori hanno l'ente a null
                ru = RuoloUtente.objects.create(utente=user, ruolo=gruppo, ente=None)
                ru.save()
                messages.success(request, 'Registrazione avvenuta con successo')
                return HttpResponseRedirect(reverse('albdif:login'))
        except Exception as e:
            messages.error(request, "Non è stato possibile creare l'utente, rivolgersi all'assistenza")
            logger.debug(e)

        messages.warning(request, 'Sono presenti degli errori')
        return render(request, self.template_name, {
            'form': registrazione_form,
        })


class registrazione_titolare(generic.DetailView):
    """
    # Gestisce la pagina di richiesta registrazione da parte di Titolare altro AD Partner
    """
    template_name = "albdif/form_registrazione_titolare.html"

    def get(self, request, *args, **kwargs):

        registrazione_form = RegistrazioneForm()
        richiesta_form = RegistrazioneTitolareForm()
        return render(request, self.template_name, {
            'form': registrazione_form,
            'form_richiesta': richiesta_form,
        })

    def post(self, request, *args, **kwargs):
        try:
            registrazione_form = RegistrazioneForm(request.POST)
            richiesta_form = RegistrazioneTitolareForm(request.POST, request.FILES)
            if registrazione_form.is_valid():
                user_data = registrazione_form.cleaned_data
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password'],
                        #first_name=user_data['first_name'],
                        #last_name=user_data['last_name']
                    )
                    # crea il visitatore legandolo all'utente appena registrato
                    v = Visitatore.objects.create(utente=user, registrazione=datetime.now())
                    # salva l'istanza
                    v.save()

                    #richiesta_form = RegistrazioneTitolareForm(request.POST, request.FILES)
                    if richiesta_form.is_valid():
                        # salva la Richiesta Adesione al sito
                        richiesta_data = richiesta_form.cleaned_data
                        RichiestaAdesione.objects.create(
                            utente=user,
                            richiesta_adesione=richiesta_data['richiesta_adesione'],
                        )

                        #@TODO Per adesso si assegna subito il ruolo Titolare ma successivamente sarà fatto all'approvazione
                        # preleva il gruppo/ruolo dell'utente
                        gruppo = Group.objects.filter(name="Titolare").first()
                        # crea il ruolo dell'utente sul sito (i visitatori hanno l'ente a null
                        ru = RuoloUtente.objects.create(utente=user, ruolo=gruppo, ente=None)
                        ru.save()
                        messages.success(request, 'Registrazione avvenuta con successo')
                        return HttpResponseRedirect(reverse('albdif:login'))
                    else:
                        # effettuo la rollback per non lasciare l'utente censito parzialmente
                        transaction.set_rollback(True)
        except Exception as e:
            logger.debug(e)
            raise ValidationError("Sono presenti degli errori")

        messages.error(request, "Registrazione non avvenuta: verificare gli errori")
        return render(request, self.template_name, {
            'form': registrazione_form,
            'form_richiesta': richiesta_form,
        })


class contatti(View):
    """
    # Gestisce la pagina dei contatti per la richiesta informazioni
    """
    template_name = "albdif/contatti.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Richiesta inviata con successo')
        return redirect('albdif:home')


class profilo(LoginRequiredMixin, generic.DetailView):
    """
    # Gestisce la pagina dell'utente
    """
    model = User
    template_name = "albdif/profilo.html"
    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        """ La pagina del profilo può essere acceduta solo dal suo utente """
        if self.get_object() != request.user:
            messages.warning(request, 'Accesso ad altre pagine profilo non consentito!')
            return redirect('albdif:home')
            #raise PermissionDenied("Accesso ad altre pagine profilo non consentito")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Ritorna la lista delle prenotazioni di un utente"""
        context = super(profilo, self).get_context_data(**kwargs)
        utente_id = self.kwargs.get('pk')
        prenotazioni = CalendarioPrenotazione.objects.filter(prenotazione__visitatore__utente__id=utente_id,
                                                             data_inizio__gte=datetime.now())
        storico = CalendarioPrenotazione.objects.filter(prenotazione__visitatore__utente__id=utente_id,
                                                        data_inizio__lt=datetime.now())
        context['prenotazioni_list'] = prenotazioni
        context['storico_list'] = storico
        return context


class proprieta_detail(generic.ListView):
    """
    Gestisce la pagina di dettaglio di una Proprietà (Albergo Diffuso)
    - ritorna la lista delle camere dell'AD selezionato ordinata per descrizione
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
    Gestisce la pagina di dettaglio di una Proprietà Partner (Albergo Diffuso)
    - ritorna la lista dei partner con le foto della proprietà
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


class camera_detail(generic.DetailView):
    """
    Gestisce le camere di una proprietà
    - estraggo solo i periodi di prenotazione che comprendono la data corrente e i futuri
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
        prenotazioni = []
        if self.request.user.is_authenticated:
            prenotazioni = CalendarioPrenotazione.objects.filter(prenotazione__visitatore__utente=self.request.user,
                                                                 prenotazione__camera=self.object,
                                                                 data_inizio__gte=datetime.now())
        context['disabled_dates'] = json.dumps(gia_prenotate)
        context['foto'] = foto
        context['servizi'] = ServizioCamera.objects.filter(camera=self.object)
        context['prenotazioni_list'] = prenotazioni
        return context


class prenota_camera(generic.DetailView):
    """
    Gestisce la pagina del form di prenotazione con i form Prenotazione e CalendarioPrenotazione
    """
    template_name = "albdif/form_prenotazione.html"

    def get(self, request, *args, **kwargs):
        visitatore = Visitatore.objects.get(utente__id=self.kwargs["id1"])
        camera = get_object_or_404(Camera, id=self.kwargs["id2"])
        prenotazione_form = PrenotazioneForm(initial={'visitatore': visitatore.id, 'camera': camera.id})
        calendario_form = CalendarioPrenotazioneForm()
        stagioni = Stagione.objects.filter(data_fine__gt=datetime.now()).order_by("data_inizio")
        return render(request, self.template_name, {
            'visitatore': visitatore,
            'camera': camera,
            'prenotazione_form': prenotazione_form,
            'calendario_form': calendario_form,
            'stagioni': stagioni
        })

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        visitatore = Visitatore.objects.get(utente__id=self.kwargs["id1"])
        camera = get_object_or_404(Camera, id=self.kwargs["id2"])

        prenotazione_form = PrenotazioneForm(request.POST)
        prenotazione_form.instance.visitatore = visitatore
        prenotazione_form.instance.camera = camera
        prenotazione_form.instance.stato_prenotazione = Prenotazione.REGISTRATA
        prenotazione_form.instance.data_prenotazione = datetime.now()

        calendario_form = CalendarioPrenotazioneForm(request.POST)
        calendario_form.instance.prenotazione = prenotazione_form.instance
        stagioni = Stagione.objects.filter(data_fine__gt=datetime.now()).order_by("data_inizio")

        if prenotazione_form.is_valid() and calendario_form.is_valid():
            prenotazione = prenotazione_form.save()
            calendario = calendario_form.save(commit=False)
            calendario.prenotazione = prenotazione
            calendario.save()
            messages.success(request, 'Prenotazione avvenuta con successo')
            #@TODO invio email all'utente
            return HttpResponseRedirect(reverse('albdif:profilo', kwargs={'pk': visitatore.utente.id}))
        else:
            messages.error(request, 'Sono presenti degli errori: ricontrollare i dati inseriti')

        return render(request, self.template_name, {
            'visitatore': visitatore,
            'camera': camera,
            'prenotazione_form': prenotazione_form,
            'calendario_form': calendario_form,
            'stagioni': stagioni
        })


class prenota_modifica(generic.DetailView):
    """
    Gestisce la modifica di una prenotazione
    """
    template_name = "albdif/form_prenotazione_modifica.html"

    def dispatch(self, request, *args, **kwargs):
        """ La pagina della prenotazione può essere acceduta solo dal suo utente """
        prenotazione = get_object_or_404(Prenotazione, id=self.kwargs["id1"])
        if prenotazione.visitatore.utente.id != request.user.id:
            messages.warning(request, 'Accesso ad altre pagine prenotazione non consentito!')
            return HttpResponseRedirect(reverse('albdif:camera_detail', kwargs={'pk': prenotazione.camera.id}))

        """ Non è possibile modificare una prenotazione già pagata"""
        p = get_object_or_404(Prenotazione, id=self.kwargs["id1"])
        if p.stato_prenotazione == "PG":
            messages.warning(request, 'Non è possibile modificare una prenotazione già pagata!')
            return HttpResponseRedirect(reverse('albdif:camera_detail', kwargs={'pk': prenotazione.camera.id}))

        """ Non è possibile modificare una prenotazione passata"""
        cp = CalendarioPrenotazione.objects.filter(prenotazione__id=self.kwargs["id1"]).order_by("data_inizio").first()
        if cp.data_inizio < datetime.today().date():
            messages.warning(request, 'Non è possibile modificare una prenotazione passata!')
            return HttpResponseRedirect(reverse('albdif:camera_detail', kwargs={'pk': prenotazione.camera.id}))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        prenotazione = get_object_or_404(Prenotazione, id=self.kwargs["id1"])
        calendario = get_object_or_404(CalendarioPrenotazione, prenotazione__id=prenotazione.id)
        visitatore = get_object_or_404(Visitatore, id=prenotazione.visitatore.id)
        camera = get_object_or_404(Camera, id=prenotazione.camera.id)
        prenotazione_form = PrenotazioneForm(instance=prenotazione)
        calendario_form = CalendarioPrenotazioneForm(instance=calendario)
        stagioni = Stagione.objects.filter(data_fine__gt=datetime.now()).order_by("data_inizio")

        return render(request, self.template_name, {
            'visitatore': visitatore,
            'camera': camera,
            'prenotazione_form': prenotazione_form,
            'calendario_form': calendario_form,
            'stagioni': stagioni
        })

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        prenotazione = get_object_or_404(Prenotazione, id=self.kwargs["id1"])

        calendario = get_object_or_404(CalendarioPrenotazione, prenotazione__id=prenotazione.id)
        visitatore = get_object_or_404(Visitatore, id=prenotazione.visitatore.id)
        camera = get_object_or_404(Camera, id=prenotazione.camera.id)
        stagioni = Stagione.objects.filter(data_fine__gt=datetime.now()).order_by("data_inizio")
        st = []
        for s in stagioni:
            e = {'stagione': s.stagione, 'data_inizio': s.data_inizio, 'data_fine': s.data_fine,
                 'prezzo_default': s.prezzo_default}
            st.append(e)

        tot = calcola_prezzo_totale(calendario.data_inizio, calendario.data_fine, st)
        if prenotazione.costo_soggiorno and prenotazione.costo_soggiorno != tot:
            prenotazione.costo_soggiorno = tot
            prezzo_aggiornato = True
        else:
            prezzo_aggiornato = False

        prenotazione_form = PrenotazioneForm(request.POST, instance=prenotazione)
        calendario_form = CalendarioPrenotazioneForm(request.POST, instance=calendario)

        if prenotazione_form.is_valid() and calendario_form.is_valid():
            prenotazione_form.save()
            calendario_form.save()
            messages.success(request, 'Prenotazione modificata con successo')
            if prezzo_aggiornato:
                messages.info(request, 'Il prezzo è stato aggiornato')
            #@TODO invio email all'utente
            return HttpResponseRedirect(reverse('albdif:profilo', kwargs={'pk': visitatore.utente.id}))

        return render(request, self.template_name, {
            'visitatore': visitatore,
            'camera': camera,
            'prenotazione_form': prenotazione_form,
            'calendario_form': calendario_form,
            'stagioni': stagioni
        })


class prenota_cancella(generic.DetailView):
    """
    Gestisce la cancellazione di una prenotazione
    """
    template_name = "albdif/camera_detail.html"

    def dispatch(self, request, *args, **kwargs):
        """ La pagina della prenotazione può essere acceduta solo dal suo utente """
        prenotazione = get_object_or_404(Prenotazione, id=self.kwargs["id1"])
        if prenotazione.visitatore.utente.id != request.user.id:
            messages.error(request, 'Accesso ad altre pagine prenotazione non consentito!')
            return HttpResponseRedirect(reverse('albdif:camera_detail', kwargs={'pk': prenotazione.camera.id}))

        """ Non è possibile cancellare una prenotazione già pagata"""
        p = get_object_or_404(Prenotazione, id=self.kwargs["id1"])
        if p.stato_prenotazione == "PG":
            messages.warning(request, 'Non è possibile cancellare una prenotazione già pagata!')
            return HttpResponseRedirect(reverse('albdif:camera_detail', kwargs={'pk': prenotazione.camera.id}))

        """ Non è possibile cancellare una prenotazione passata"""
        cp = CalendarioPrenotazione.objects.filter(prenotazione__id=self.kwargs["id1"]).order_by("data_inizio").first()
        if cp.data_inizio < datetime.today().date():
            messages.warning(request, 'Non è possibile cancellare una prenotazione passata!')
            return HttpResponseRedirect(reverse('albdif:camera_detail', kwargs={'pk': prenotazione.camera.id}))

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        p = get_object_or_404(Prenotazione, id=self.kwargs["id1"])
        return p

    def get(self, request, *args, **kwargs):
        prenotazione = self.get_queryset()
        prenotazione.stato_prenotazione = prenotazione.CANCELLATA

        prenotazione.save()
        messages.success(request, 'Prenotazione cancellata con successo')

        return HttpResponseRedirect(reverse('albdif:camera_detail', kwargs={'pk': prenotazione.camera.id}))


class prenota_paga(generic.DetailView):
    """
    Gestisce la conferma / pagamento di una prenotazione
    """
    template_name = "albdif/form_pagamento.html"

    def dispatch(self, request, *args, **kwargs):
        """ La pagina del pagamento della prenotazione può essere acceduta solo dal suo utente """
        prenotazione = get_object_or_404(Prenotazione, id=self.kwargs["id1"])
        if prenotazione.visitatore.utente.id != request.user.id:
            messages.warning(request, 'Accesso ad altre pagine prenotazione non consentito!')
            return HttpResponseRedirect(reverse('albdif:camera_detail', kwargs={'pk': prenotazione.camera.id}))

        """ Il pagamento è stato già effettuato"""
        p = get_object_or_404(Prenotazione, id=self.kwargs["id1"])
        if p.stato_prenotazione == "PG":
            messages.warning(request, 'Il pagamento risulta già effettuato!')
            return HttpResponseRedirect(reverse('albdif:camera_detail', kwargs={'pk': prenotazione.camera.id}))

        """ Non è possibile modificare una prenotazione passata"""
        cp = CalendarioPrenotazione.objects.filter(prenotazione__id=self.kwargs["id1"]).order_by("data_inizio").first()
        if cp.data_inizio < datetime.today().date():
            messages.warning(request, 'Non è possibile modificare una prenotazione passata!')
            return HttpResponseRedirect(reverse('albdif:camera_detail', kwargs={'pk': prenotazione.camera.id}))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        prenotazione = get_object_or_404(Prenotazione, id=self.kwargs["id1"])
        calendario = get_object_or_404(CalendarioPrenotazione, prenotazione__id=prenotazione.id)
        visitatore = get_object_or_404(Visitatore, id=prenotazione.visitatore.id)
        camera = get_object_or_404(Camera, id=prenotazione.camera.id)
        stagioni = Stagione.objects.filter(data_fine__gt=datetime.now()).order_by("data_inizio")
        if prenotazione.costo_soggiorno is None:
            prenotazione.costo_soggiorno = calcola_prezzo_totale(calendario.data_inizio, calendario.data_fine, stagioni)
        pagamento_form = PagamentoForm(instance=prenotazione)

        return render(request, self.template_name, {
            'visitatore': visitatore,
            'camera': camera,
            'pagamento_form': pagamento_form,
        })

    def post(self, request, *args, **kwargs):
        prenotazione = get_object_or_404(Prenotazione, id=self.kwargs["id1"])
        visitatore = get_object_or_404(Visitatore, id=prenotazione.visitatore.id)
        camera = get_object_or_404(Camera, id=prenotazione.camera.id)
        pagamento_form = PagamentoForm(request.POST, instance=prenotazione)

        if pagamento_form.is_valid():
            prenotazione.data_pagamento = datetime.now()
            prenotazione.stato_prenotazione = prenotazione.CONFERMATA
            pagamento = pagamento_form.save()
            messages.success(request, 'Pagamento effettuto con successo')
            #@TODO invio email all'utente
            return HttpResponseRedirect(reverse('albdif:profilo', kwargs={'pk': visitatore.utente.id}))

        return render(request, self.template_name, {
            'visitatore': visitatore,
            'camera': camera,
            'pagamento_form': pagamento_form,
        })


class camere_list(generic.ListView):
    """
    Gestisce le camere della proprietà principale
    - ritorna la lista delle camere dell'AD principale ordinata per descrizione
    """
    template_name = "albdif/camere_list.html"
    context_object_name = "camere_list"

    def get_queryset(self):
        return Camera.objects.filter(proprieta__principale=True).order_by("descrizione")


class prezzo_camera_detail(generic.DetailView):
    """
    Gestisce il prezzo specifico di una camera:
    @TODO TBD
    """
    model = PrezzoCamera
    template_name = "albdif/prezzo_camera_detail.html"


class prezzi_camera_list(generic.ListView):
    """
    Ritorna la lista dei prezzi di una camera
    @TODO TBD - modificare per accettare parametro ed elencare solo i prezzi di una camera
    """
    template_name = "albdif/prezzi_camera_list.html"
    context_object_name = "prezzi_camera_list"

    def get_queryset(self):
        return PrezzoCamera.objects.order_by("camera.descrizione")


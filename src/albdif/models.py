from datetime import datetime

from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import CharField, Q
from django.core.exceptions import ValidationError


class Visitatore(models.Model):
    """
    Visitatore:
    la persona che utilizza il sito:
        - i visitatori che effettuano la registrazione al sito per prenotare
        - i titolari delle proprietà/camere degli AD Partner
        - altre persone che useranno l'applicazione (es. Accoglienza, Manutenzione, Pulizia, etc.)
    """
    utente = models.OneToOneField(User, on_delete=models.CASCADE)
    # timestamp della registrazione al sito
    registrazione = models.DateTimeField()
    # recapito telefonico
    telefono = models.CharField(max_length=20, null=True, blank=True)
    # codice fiscale
    codice_fiscale = models.CharField(max_length=16, null=True, blank=True)
    # partita iva
    partita_iva = models.CharField(max_length=11, null=True, blank=True)

    class Meta():
        verbose_name = "Visitatore"
        verbose_name_plural = "Visitatori"

    def __str__(self):
        return f"{self.utente.last_name} {self.utente.first_name}"

    @property
    def is_titolare(self):
        # ritorna True se l'utente è Titolare
        gruppo = Group.objects.get(name="Titolare")
        return RuoloUtente.objects.filter(ruolo=gruppo, utente=self.utente).exists()

    @property
    def proprieta(self):
        # ritorna elenco delle Proprietà
        gruppo = Group.objects.get(name="Titolare")
        return RuoloUtente.objects.filter(ruolo=gruppo, utente=self.utente)


class RichiestaAdesione(models.Model):
    """
    RichiestaAdesione:
        l'utente che richiede di associarsi al sito per pubblicare il suo Albergo Diffuso (Partner)
    """
    utente = models.OneToOneField(User, on_delete=models.CASCADE)
    # richiesta adesione
    richiesta_adesione = models.FileField(upload_to='adesioni')
    # timestamp richiesta adesione
    data_richiesta = models.DateTimeField(default=datetime.now)
    # approvazione adesione
    approvazione_adesione = models.FileField(null=True, blank=True, upload_to='approvazioni')
    # timestamp approvazione adesione
    data_adesione = models.DateTimeField(null=True, blank=True)

    class Meta():
        verbose_name = "Richiesta adesione"
        verbose_name_plural = "Richieste adesioni"

    def __str__(self):
        return f"{self.utente.last_name} {self.data_richiesta}"


class Proprieta(models.Model):
    """
    Proprietà:
    l'albergo diffuso di proprietà di un host necessario per collezionare le camere da affittare
    """
    # descrizione della struttura ricettiva (Albergo Diffuso)
    descrizione = models.CharField(max_length=2000)
    # indica se l'albergo è quello principale (solo un AD può avere questo attributo a True)
    principale = models.BooleanField(default=False, help_text="Indica se è l'AD principale")
    # nome della struttura ricettiva
    nome = models.CharField(max_length=100, default="... inserire un nickname")

    class Meta():
        verbose_name = "Proprietà"
        verbose_name_plural = "Proprietà"

    def __str__(self):
        return f"{self.nome}"
    
    def clean(self):
        if self.principale and Proprieta.objects.filter(principale=True).exclude(id=self.id).exists():
            raise ValidationError("Esiste già una proprietà principale.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Proprieta, self).save(*args, **kwargs)

    @property
    def host(self):
        # ritorna il Titolare proprietario dell'AD Partner
        if not self.principale:
            return RuoloUtente.objects.filter(ruolo="Titolare", ente=self.pk).first()
        else:
            return None

    @property
    def prenotazioni(self):
        # ritorna elenco delle prenotazioni attive
        return CalendarioPrenotazione.objects.filter(prenotazione__camera__proprieta=self.pk,
                                                     data_inizio__gte=datetime.now()).order_by('data_inizio')

class RuoloUtente(models.Model):
    """
    RuoloUtente:
    definisce il ruolo di un utente su una proprietà (AD); in base al ruolo si possono abilitare
    o meno delle funzionalità dell'applicazione
    """
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    ruolo = models.ForeignKey(Group, on_delete=models.CASCADE)
    ente = models.ForeignKey(Proprieta, on_delete=models.CASCADE, null=True, blank=True)

    class Meta():
        verbose_name = "Ruolo utente"
        verbose_name_plural = "Ruoli utente"
        unique_together = ('utente', 'ente')


    def __str__(self):
        return f"{self.utente}"


class Servizio(models.Model):
    """
    Servizio:
    definisce i servizi che possono essere forniti (differenti per ogni camera)
    """
    descrizione_servizio = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.descrizione_servizio}"

    class Meta():
        verbose_name = "Servizio"
        verbose_name_plural = "Servizi"


class Camera(models.Model):
    """
    Camera:
    ogni camera fa parte di una proprietà (Albergo Diffuso)
    """
    # nome della camera (facilita l'identificazione da parte della struttura ricettiva e del cliente)
    nome = models.CharField(max_length=100, default="... inserire un nickname")
    # descrizione della camera (utile ai clienti per capire cosa stanno prenotando)
    descrizione = models.CharField(max_length=1000)
    # numero dei posti letto presenti nella camera
    numero_posti_letto = models.IntegerField(null=True, blank=True, default=2)
    # proprietà (albergo diffuso) a cui appartiene la camera
    proprieta = models.ForeignKey(Proprieta, on_delete=models.CASCADE)

    class Meta():
        verbose_name = "Camera"
        verbose_name_plural = "Camere"

    def __str__(self):
        return f"{self.nome}"

    @property
    def image(self):
        "ritorna l'elenco delle foto della camera"
        return Foto.objects.filter(camera=self.pk).first()

    @property
    def prezzo_bassa_stagione(self):
        "ritorna il prezzo minimo della stagione 'Bassa'"
        stagione_bassa = Stagione.objects.filter(stagione="Bassa").first()
        if stagione_bassa:
            prezzo_camera = PrezzoCamera.objects.filter(camera=self, stagione=stagione_bassa).order_by('prezzo').first()
            if prezzo_camera:
                return prezzo_camera.prezzo
            return stagione_bassa.prezzo_default
        return None


class ServizioCamera(models.Model):
    """
    ServizioCamera
    elenca tutti i servizi di una camera specificando se sono inclusi nel prezzo (incluso=True)
    od opzionali (incluso=False), in questo caso sarà visibile il prezzo
    """
    # tipo di servizio offerto dalla camera
    servizio = models.ForeignKey(Servizio, on_delete=models.CASCADE)
    # camera a cui il servizio è associato
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    # indica se il servizio è incluso nel prezzo o meno (opzionale)
    incluso = models.BooleanField(default=False)
    # è il costo giornaliero del servizio: se "incluso" = True deve essere 0
    costo = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    class Meta():
        verbose_name = "Servizio camera"
        verbose_name_plural = "Servizi camera"

    def __str__(self):
        return f"{self.servizio}"

    def clean(self):
        if not self.incluso and (not self.costo or self.costo == 0):
            raise ValidationError("Se il servizio è opzionale va indicato il costo")

    def save(self, *args, **kwargs):
        self.clean()
        super(ServizioCamera, self).save(*args, **kwargs)


class Foto(models.Model):
    """
    Foto:
    ogni foto può essere riferita o ad una camera o alla proprietà
    """
    # descrizione della foto
    descrizione = CharField(max_length=100)
    # camera oggetto della foto
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, null=True, blank=True)
    # proprietà (albergo) oggetto della foto
    proprieta = models.ForeignKey(Proprieta, on_delete=models.CASCADE, null=True, blank=True)
    # file immagine
    file = models.FileField(blank=True, upload_to='foto_camera')

    class Meta():
        verbose_name = "Foto"
        verbose_name_plural = "Foto"

    def __str__(self):
        if self.camera:
            return f"{self.descrizione} di {self.camera} - camera: "
        else:
            return f"{self.descrizione} di {self.proprieta} - proprietà: "


class Prenotazione(models.Model):
    """
    Prenotazione:
    la prenotazione viene eseguita da un visitatore per una camera di una proprietà
    Stati della prenotazione:

    - REGISTRATA   - è lo stato iniziale della prenotazione                             (START)   'PR' *
    - CANCELLATA   - è lo stato che assume a seguito della transizione di cancellazione (END)     'CA' *
    - CONFERMATA   - è lo stato che determina la fine della transazione di pagamento              'PG' *
    - RICH.RIMB.   - è lo stato che assume a seguito della richiesta di rimborso                  'RR'
    - RIMBORSATA   - è lo stato che assume al termine della transizione di rimborso     (END)     'RE'
    - NEGATA       - è lo stato che assume dopo la richiesta di rimborso                (END)     'NG'
    - SCADUTA      - è lo stato che assume se la prenotazione non viene confermata entro x giorni 'SC'

    N.B. Solo gli stati con l'asterisco in fondo sono quelli gestiti dall'applicazione per il PW
    """

    REGISTRATA = "PR"
    CONFERMATA = "PG"
    CANCELLATA = "CA"
    RICHIESTA = "RR"
    RIMBORSATA = "RE"
    NEGATA = "NE"
    SCADUTA = "SC"

    STATO_PRENOTAZIONE = [
        (REGISTRATA, "Registrata"),
        (CONFERMATA, "Confermata e Pagata"),
        (CANCELLATA, "Cancellata"),
        (RICHIESTA, "Richiesta Rimborso"),
        (RIMBORSATA, "Rimborsata"),
        (NEGATA, "Negata"),
        (SCADUTA, "Scaduta")
    ]

    PASSAGGI_STATO = [
        (REGISTRATA, REGISTRATA),
        (REGISTRATA, CONFERMATA),
        (REGISTRATA, CANCELLATA),
        (REGISTRATA, SCADUTA),
        (CONFERMATA, RICHIESTA),
        (RICHIESTA, RIMBORSATA),
        (RICHIESTA, NEGATA),
    ]
    # l'utente che esegue una prenotazione ...
    visitatore = models.ForeignKey(Visitatore, on_delete=models.CASCADE)
    # la camera oggetto della prenotazione
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    # data registrazione della prenotazione
    data_prenotazione = models.DateTimeField()
    # indica lo stato attuale della prenotazione
    stato_prenotazione = models.CharField(max_length=2, choices=STATO_PRENOTAZIONE, default=REGISTRATA)
    # eventuale richiesta del cliente
    richiesta = models.CharField(max_length=1000, null=True, blank=True, help_text="richiesta aggiuntiva del cliente")
    # indica il costo del soggiorno determinato al momento della registrazione
    costo_soggiorno = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    # indica il timestamp in cui è stato effettuato il pagamento del soggiorno
    data_pagamento = models.DateTimeField(null=True, blank=True)
    # numero delle persone che saranno ospitati
    numero_persone = models.IntegerField(null=True, blank=True, default=1)
    # timestamp cambio di stato
    data_stato = models.DateTimeField(null=True, blank=True)

    class Meta():
        verbose_name = "Prenotazione"
        verbose_name_plural = "Prenotazioni"

    def __str__(self):
        return f"{self.id} {self.visitatore} {self.camera} {self.stato_prenotazione}"

    def is_valid_state_transition(self, old_state, new_state):
        return (old_state, new_state) in self.PASSAGGI_STATO

    def clean(self):
        if self.pk:
            old_state = Prenotazione.objects.get(pk=self.pk).stato_prenotazione
            if not self.is_valid_state_transition(old_state, self.stato_prenotazione):
                raise ValidationError(f"Passaggio di stato non consentito da {old_state} a {self.stato_prenotazione}")
            self.data_stato = datetime.now()

    def save(self, *args, **kwargs):
        self.clean()
        super(Prenotazione, self).save(*args, **kwargs)


class CalendarioPrenotazione(models.Model):
    """
    CalendarioPrenotazione:
    registra i periodi relativi ad una prenotazione
    """
    prenotazione = models.ForeignKey(Prenotazione, on_delete=models.CASCADE)
    # data inizio soggiorno
    data_inizio = models.DateField(help_text="Data inizio soggiorno")
    # data fine soggiorno
    data_fine = models.DateField(help_text="Data fine soggiorno")

    class Meta():
        verbose_name = "Calendario della prenotazione"
        verbose_name_plural = "Calendario della prenotazione"

    def __str__(self):
        return f"{self.prenotazione} {self.data_inizio} {self.data_fine}"

    def altra_prenotazione_presente(self, data_inizio, data_fine, prenotazione):
        cp = CalendarioPrenotazione.objects.filter(
            Q(data_inizio__lte=data_fine),
            Q(data_fine__gt=data_inizio),
            ~Q(prenotazione__stato_prenotazione="CA"),
            Q(prenotazione__camera__pk=prenotazione.camera.pk),
            ~Q(prenotazione__id=prenotazione.id)
        )
        return cp.exists()

    def clean(self):
        if self.pk:
            prenotazione = Prenotazione.objects.get(pk=self.prenotazione.pk)
            if self.altra_prenotazione_presente(self.data_inizio, self.data_fine, prenotazione):
                raise ValidationError(f"Trovata altra prenotazione nello stesso periodo")

        if not (self.data_fine and self.data_inizio):
            raise ValidationError("Inserire le date di soggiorno")

        if self.data_fine <= self.data_inizio:
            raise ValidationError("La data fine deve essere maggiore della data inizio")

    def save(self, *args, **kwargs):
        self.clean()
        super(CalendarioPrenotazione, self).save(*args, **kwargs)


class Stagione(models.Model):
    """
    Stagione:
    definisce le stagioni (periodi) che determinano poi i prezzi
    """
    BASSA = "Bassa"
    MEDIA = "Media"
    ALTA = "Alta"

    PREZZI_STAGIONE = [(BASSA, "Bassa stagione"), (MEDIA, "Media stagione"), (ALTA, "Alta stagione")]

    # stagione (un nome per ricordare un periodo dell'anno)
    stagione = models.CharField(max_length=50, choices=PREZZI_STAGIONE)
    # data inizio della stagione
    data_inizio = models.DateField()
    # data fine della stagione
    data_fine = models.DateField()
    # prezzo di riferimento
    prezzo_default = models.DecimalField(max_digits=7, decimal_places=2, default=50)

    class Meta():
        verbose_name = "Stagione"
        verbose_name_plural = "Stagioni"

    def __str__(self):
        return f"{self.stagione} {self.data_inizio} {self.data_fine}"

    def clean(self):
        if self.data_fine < self.data_inizio:
            raise ValidationError("La data fine deve essere maggiore della data inizio")

        s = 0 if not self.id else self.id
        if Stagione.objects.filter(Q(data_inizio__lte=self.data_fine),
                                   Q(data_fine__gte=self.data_inizio),
                                   ~Q(id__exact=s)).exists():
            raise ValidationError("Le date si sovrappongono ad un'altra stagione")

    def save(self, *args, **kwargs):
        self.clean()
        super(Stagione, self).save(*args, **kwargs)


class PrezzoCamera(models.Model):
    """
    PrezzoCamera:
    indica il prezzo della camera relativo ad ogni stagione
    """
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    stagione = models.ForeignKey(Stagione, on_delete=models.CASCADE)
    # prezzo specifico di una camera per una stagione
    prezzo = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta():
        verbose_name = "Prezzo della camera"
        verbose_name_plural = "Prezzo delle camere"

    def __str__(self):
        return f"{self.camera} {self.stagione} {self.prezzo}"
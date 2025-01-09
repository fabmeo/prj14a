from functools import cached_property
from typing import Optional, Any

from django.contrib.auth.models import User, Group as Group_, AbstractUser, Permission
from django.db import models
from django.db.models import CharField, Q, QuerySet
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

valida_telefono = RegexValidator(r"^\d[1-9]{1,3}/\d{7,10}$")


# class Visitatore(models.Model):
#     """
#     Visitatore:
#     persona che effettua la registrazione al sito per effettuare la prenotazione
#     """
#     # timestamp della registrazione al sito
#     registrazione = models.DateTimeField()
#     utente = models.OneToOneField(User, on_delete=models.CASCADE)
#     telefono = models.CharField(max_length=20, null=True, blank=True)
#     codice_fiscale = models.CharField(max_length=16, null=True, blank=True)
#
#     class Meta():
#         verbose_name = "Visitatore"
#         verbose_name_plural = "Visitatori"
#
#     def __str__(self):
#         return f"{self.utente.last_name} {self.utente.first_name}"
#
#
# class Host(models.Model):
#     """
#     Host:
#     persona o azienda che effettua la registrazione per accedere ai servizi hosting dell'AD
#     """
#     # timestamp della registrazione al sito
#     registrazione = models.DateTimeField()
#     utente = models.OneToOneField(User, on_delete=models.CASCADE)
#     telefono = models.CharField(max_length=20, null=True, blank=True)
#     codice_fiscale = models.CharField(max_length=16, null=True, blank=True)
#     partita_iva = models.CharField(max_length=11, null=True, blank=True)
#     # contratto di associazione al sito
#     contratto = models.FileField(blank=True, upload_to='contratti_host', null=True)
#     # richiesta di associazione al sito
#     richiesta_associazione = models.FileField(blank=True, upload_to='richiesta_host', null=True)
#
#     class Meta():
#         verbose_name = "Host"
#         verbose_name_plural = "Hosts"
#
#     def __str__(self):
#         return f"{self.utente.last_name} {self.utente.first_name}"


class Proprieta(models.Model):
    """
    Proprietà:
    l'albergo diffuso di proprietà di un host necessario per collezionare le camere da affittare
    """
    # nome della struttura ricettiva
    nome = models.CharField(max_length=100, default="... inserire un nickname")
    # descrizione della struttura ricettiva (Albergo Diffuso)
    descrizione = models.CharField(max_length=2000)
    # indica se l'albergo è quello principale (solo un AD può avere questo attributo a True)
    principale = models.BooleanField(default=False, help_text="Indica se è l'AD principale")

    class Meta():
        verbose_name = "Proprietà"
        verbose_name_plural = "Proprietà"

    def __str__(self):
        return f"{self.descrizione[:20]}"
    
    def clean(self):
        if self.principale and Proprieta.objects.filter(principale=True).exclude(id=self.id).exists():
            raise ValidationError("Esiste già una proprietà principale.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Proprieta, self).save(*args, **kwargs)
        

class Group(Group_):
    class Meta:
        proxy = True


class Utente(AbstractUser):
    # timestamp della registrazione al sito
    registrazione = models.DateTimeField()
    # codice fiscale
    codice_fiscale = models.CharField(max_length=16, null=True, blank=True)
    # partita iva
    partita_iva = models.CharField(max_length=11, null=True, blank=True)
    # numero di telefono
    telefono = models.CharField("Telefono", max_length=255, blank=True, null=True,
        validators=[valida_telefono],
        help_text="Deve contenere solo numeri e uno slash ( / )",
    )
    # richiesta di associazione al sito
    richiesta_associazione = models.FileField(blank=True, upload_to='richiesta_host', null=True)
    # contratto di associazione al sito
    contratto = models.FileField(blank=True, upload_to='contratti_host', null=True)
    groups = models.ManyToManyField(Group, related_name='albdif_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='albdif_user_set_permissions')

    class Meta:
        permissions = (
            ("Visitatore", "Gestione visitatore"),
            ("Titolare", "Titolare di proprietà"),
            ("Contabile", "Gestore contabilità proprietà"),
            ("Accoglienza", "Accoglienza visitatori di una proprietà"),
        )

    def get_label(self) -> str:
        if self.last_name and self.first_name:
            return f"{self.first_name} {self.last_name}"
        return str(self.username)

    def get_proprieta(self) -> Optional[Proprieta]:
        return self.get_allowed_proprieta().first()

    @cached_property
    def default_proprieta(self) -> Optional[Proprieta]:
        return self.get_proprieta().first()

    def get_allowed_proprieta(self, **extra: Any) -> QuerySet:
        if RuoloUtente.objects.filter(user=self, ente__isnull=True):
            return Proprieta.objects.filter(**extra)  # type: ignore[no-any-return]

        return Proprieta.objects.filter(**extra)  # type: ignore[no-any-return]
        #return Proprieta.objects.filter(userrole__user=self).filter(**extra)  # type: ignore[no-any-return]


class RuoloUtente(models.Model):
    """
    Ruolo che un utente svolge nell'usare l'applicazione
    es.
       - l'utente con ruolo (Django Group) "Visitatore" del sito                   - GESTITO IN QUESTA VERSIONE
       - l'utente con ruolo (Django Group) "Titolare" di una proprietà (Host)      - GESTITO IN QUESTA VERSIONE
       - l'utente con ruolo (Django Group) "Responsabile Ordini" di una proprietà
       - l'utente con ruolo (Django Group) "Contabile" di una proprietà
       - l'utente con ruolo (Django Group) "Accoglienza" di una proprietà
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    ente = models.ForeignKey(
        Proprieta, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={"parent__isnull": True}
    )

    def __str__(self):
        return f"{self.group}"

    class Meta():
        verbose_name = "Ruolo utente"
        verbose_name_plural = "Ruoli utente"


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
    ogni camera fa parte di una proprietà
    """
    proprieta = models.ForeignKey(Proprieta, on_delete=models.CASCADE)
    # nome della camera (facilita l'identificazione da parte della struttura ricettiva e del cliente)
    nome = models.CharField(max_length=100, default="... inserire un nickname")
    # descrizione della camera (utile ai clienti per capire cosa stanno prenotando)
    descrizione = models.CharField(max_length=1000)
    # numero dei posti letto presenti nella camera
    numero_posti_letto = models.IntegerField(null=True, blank=True, default=2)

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
    o opzionali (incluso=False), in questo caso sarà visibile il prezzo
    """
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    servizio = models.ForeignKey(Servizio, on_delete=models.CASCADE)
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
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, null=True, blank=True)
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
        (CONFERMATA, "Confermata"),
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

    #visitatore = models.ForeignKey(Visitatore, on_delete=models.CASCADE)
    visitatore = models.ForeignKey(Utente, on_delete=models.CASCADE)
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

    class Meta():
        verbose_name = "Prenotazione"
        verbose_name_plural = "Prenotazioni"

    def __str__(self):
        return f"{self.id} {self.user} {self.camera} {self.stato_prenotazione}"

    def is_valid_state_transition(self, old_state, new_state):
        return (old_state, new_state) in self.PASSAGGI_STATO

    def clean(self):
        if self.pk:
            old_state = Prenotazione.objects.get(pk=self.pk).stato_prenotazione
            if not self.is_valid_state_transition(old_state, self.stato_prenotazione):
                raise ValidationError(f"Passaggio di stato non consentito da {old_state} a {self.stato_prenotazione}")

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
            Q(prenotazione__camera__pk=prenotazione.camera.pk),
            ~Q(prenotazione__id=prenotazione.id)
        )
        return cp.exists()

    def clean(self):
        if self.pk:
            prenotazione = Prenotazione.objects.get(pk=self.prenotazione.pk)
            if self.altra_prenotazione_presente(self.data_inizio, self.data_fine, prenotazione):
                raise ValidationError(f"Trovata altra prenotazione nello stesso periodo")

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
        verbose_name_plural = "Prezzo della camere"

    def __str__(self):
        return f"{self.camera} {self.stagione} {self.prezzo}"
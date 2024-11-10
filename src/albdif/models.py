from tabnanny import verbose

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField


class Visitatore(User):
    """
    Visitatore:
    persona che effettua la registrazione al sito per effettuare la prenotazione
    """
    registrazione = models.DateTimeField("data registrazione")

    class Meta():
        verbose_name = "Visitatore"
        verbose_name_plural = "Visitatori"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Host(User):
    """
    Host:
    persona o azienda che effettua la registrazione per accedere ai servizi hosting dell'AD
    """
    registrazione = models.DateTimeField("data registrazione")

    class Meta():
        verbose_name = "Host"
        verbose_name_plural = "Host"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Proprieta(models.Model):
    """
    Proprietà:
    l'albergo diffuso di proprietà di un host necessario per collezionare le camere da affittare
    """
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    descrizione = models.CharField(max_length=200)

    class Meta():
        verbose_name = "Proprietà"
        verbose_name_plural = "Proprietà"

    def __str__(self):
        return f"{self.host} {self.descrizione}"


class Camera(models.Model):
    """
    Camera:
    ogni camera fa parte di una proprietà
    """
    proprieta = models.ForeignKey(Proprieta, on_delete=models.CASCADE)
    descrizione = models.CharField(max_length=100)

    class Meta():
        verbose_name = "Camera"
        verbose_name_plural = "Camere"

    def __str__(self):
        return f"{self.proprieta} {self.descrizione}"


class Foto(models.Model):
    """
    Foto:
    ogni foto può essere riferita o ad una camera o alla proprietà
    """
    descrizione = CharField(max_length=100)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, null=True, blank=True)
    proprieta = models.ForeignKey(Proprieta, on_delete=models.CASCADE, null=True, blank=True)
    file = models.BinaryField()

    class Meta():
        verbose_name = "Foto"
        verbose_name_plural = "Foto"

    def __str__(self):
        if self.camera:
            return f"{self.descrizione} {self.camera}"
        else:
            return f"{self.descrizione} {self.proprieta}"


class Prenotazione(models.Model):
    """
    Prenotazione:
    la prenotazione viene eseguita da un visitatore per una camera di una proprietà
    """

    PRENOTATA = "PR"
    SCADUTA = "SC"
    CANCELLATA = "CA"
    PAGATA = "PG"
    INCORSO = "IC"

    STATO_PRENOTAZIONE = {
        PRENOTATA: "Prenotata",
        SCADUTA: "Scaduta",
        CANCELLATA: "Cancellata",
        PAGATA: "Pagata",
        INCORSO: "In Corso",
    }

    visitatore = models.ForeignKey(Visitatore, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    data_prenotazione = models.DateTimeField()
    stato_prenotazione = models.CharField(max_length=2, choices=STATO_PRENOTAZIONE, default=PRENOTATA)
    richiesta = models.CharField(max_length=1000, null=True, blank=True, help_text="richiesta aggiuntiva del cliente")

    class Meta():
        verbose_name = "Prenotazione"
        verbose_name_plural = "Prenotazioni"

    def __str__(self):
        return f"{self.visitatore} {self.camera} {self.stato_prenotazione}"


class CalendarioPrenotazione(models.Model):
    """
    CalendarioPrenotazione:
    registra i periodi relativi ad una prenotazione
    """
    prenotazione = models.ForeignKey(Prenotazione, on_delete=models.CASCADE)
    data_inizio = models.DateField()
    data_fine = models.DateField()

    class Meta():
        verbose_name = "Periodo di prenotazione"
        verbose_name_plural = "Periodi di prenotazione"

    def __str__(self):
        return f"{self.prenotazione} {self.data_inizio} {self.data_fine}"


class Stagione(models.Model):
    """
    Stagione:
    definisce le stagioni (periodi) che determinano poi i prezzi
    """
    stagione = models.CharField(max_length=50)
    data_inizio = models.DateField()
    data_fine = models.DateField()

    class Meta():
        verbose_name = "Stagione"
        verbose_name_plural = "Stagioni"

    def __str__(self):
        return f"{self.stagione} {self.data_inizio} {self.data_fine}"


class PrezzoCamera(models.Model):
    """
    PrezzoCamera:
    indica il prezzo della camera relativo ad ogni stagione
    """
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    stagione = models.ForeignKey(Stagione, on_delete=models.CASCADE)
    prezzo = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta():
        verbose_name = "Prezzo della camera"
        verbose_name_plural = "Prezzo della camere"

    def __str__(self):
        return f"{self.camera} {self.stagione} {self.prezzo}"
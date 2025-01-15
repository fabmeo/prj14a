from django.contrib import admin

from .models import Visitatore, Proprieta, Camera, Foto, Prenotazione, CalendarioPrenotazione, Stagione, \
    PrezzoCamera, Servizio, ServizioCamera, RuoloUtente


class FotoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'descrizione']
    search_fields = ['descrizione', ]
    list_filter = ['proprieta__nome', 'camera__nome']


class ProprietaAdmin(admin.ModelAdmin):
    list_display = ['pk', 'nome', 'principale']
    search_fields = ['nome', 'descrizione', ]
    list_filter = ['principale', ]


class CameraAdmin(admin.ModelAdmin):
    list_display = ['pk', 'nome', 'proprieta']
    search_fields = ['descrizione', 'nome' ]
    list_filter = ['proprieta', ]


class PrenotazioneAdmin(admin.ModelAdmin):
    list_display = ['pk', 'visitatore', 'stato_prenotazione', 'data_prenotazione', 'camera', 'costo_soggiorno']
    search_fields = ['richiesta', 'visitatore']
    list_filter = ['visitatore', 'camera', 'camera__proprieta', 'stato_prenotazione', 'data_prenotazione']


class CalendarioPrenotazioneAdmin(admin.ModelAdmin):
    list_display = ['pk', 'prenotazione', 'data_inizio', 'data_fine'] #, 'prenotazione__data_prenotazione', 'prenotazione__visitatore']
    search_fields = ['prenotazione__visitatore', ]
    list_filter = ['data_inizio', 'prenotazione__visitatore', 'prenotazione__camera', 'prenotazione__stato_prenotazione']


class ServizioCameraAdmin(admin.ModelAdmin):
    list_display = ['pk', 'camera', 'servizio', 'incluso', 'costo']
    search_fields = ['camera', 'servizio']
    list_filter = ['camera', 'servizio']


class VisitatoreAdmin(admin.ModelAdmin):
    list_display = ['pk', 'utente', 'registrazione']
    search_fields = ['utente_first_name', 'utente_last_name']
    list_filter = ['registrazione',]


class RuoloUtenteAdmin(admin.ModelAdmin):
    list_display = ['utente', 'ente', 'ruolo']
    search_fields = ['utente', 'ente', 'ruolo']
    list_filter = ['ente', 'ruolo']


class StagioneAdmin(admin.ModelAdmin):
    list_display = ['pk', 'stagione', 'data_inizio', 'data_fine']
    list_filter = ['data_inizio', 'stagione', ]


admin.site.register(Stagione, StagioneAdmin)
admin.site.register(Visitatore, VisitatoreAdmin)
admin.site.register(RuoloUtente, RuoloUtenteAdmin)
admin.site.register(Foto, FotoAdmin)
admin.site.register(Proprieta, ProprietaAdmin)
admin.site.register(Camera, CameraAdmin)
admin.site.register(Prenotazione, PrenotazioneAdmin)
admin.site.register(CalendarioPrenotazione, CalendarioPrenotazioneAdmin)
admin.site.register(ServizioCamera, ServizioCameraAdmin)

admin.site.register(PrezzoCamera)
admin.site.register(Servizio)


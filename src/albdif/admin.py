from django.contrib import admin

from .models import Visitatore, Host, Proprieta, Camera, Foto, Prenotazione, CalendarioPrenotazione, Stagione, \
    PrezzoCamera


class FotoAdmin(admin.ModelAdmin):
    search_fields = ['descrizione', ]
    list_filter = ['proprieta__descrizione', 'camera__descrizione']


class ProprietaAdmin(admin.ModelAdmin):
    list_display = ['host', 'descrizione', 'principale']
    search_fields = ['descrizione', ]
    list_filter = ['principale', ]


class CameraAdmin(admin.ModelAdmin):
    list_display = ['nome', 'proprieta']
    search_fields = ['descrizione', ]
    list_filter = ['proprieta', ]


class CalendarioPrenotazioneAdmin(admin.ModelAdmin):
    list_display = ['prenotazione', 'data_inizio', 'data_fine']
    search_fields = ['prenotazione__visitatore', ]
    list_filter = ['prenotazione__visitatore', 'prenotazione__camera']


admin.site.register(Foto, FotoAdmin)
admin.site.register(Proprieta, ProprietaAdmin)
admin.site.register(Camera, CameraAdmin)
admin.site.register(CalendarioPrenotazione, CalendarioPrenotazioneAdmin)

admin.site.register(Visitatore)
admin.site.register(Host)
admin.site.register(Prenotazione)
admin.site.register(Stagione)
admin.site.register(PrezzoCamera)

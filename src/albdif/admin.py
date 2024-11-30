from django.contrib import admin

from .models import Visitatore, Host, Proprieta, Camera, Foto, Prenotazione, CalendarioPrenotazione, Stagione, \
    PrezzoCamera


class FotoAdmin(admin.ModelAdmin):
    search_fields = ['descrizione', ]
    list_filter = ['proprieta__descrizione', 'camera__descrizione']


class ProprietaAdmin(admin.ModelAdmin):
    search_fields = ['descrizione', ]
    list_filter = ['principale', ]


class CameraAdmin(admin.ModelAdmin):
    search_fields = ['descrizione', ]
    list_filter = ['proprieta', ]


admin.site.register(Foto, FotoAdmin)
admin.site.register(Proprieta, ProprietaAdmin)
admin.site.register(Camera, CameraAdmin)

admin.site.register(Visitatore)
admin.site.register(Host)
admin.site.register(Prenotazione)
admin.site.register(CalendarioPrenotazione)
admin.site.register(Stagione)
admin.site.register(PrezzoCamera)

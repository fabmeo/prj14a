from django.contrib import admin

# Register your models here.

from .models import Visitatore, Host, Proprieta, Camera, Foto, Prenotazione, CalendarioPrenotazione, Stagione, PrezzoCamera

admin.site.register(Visitatore)
admin.site.register(Host)
admin.site.register(Proprieta)
admin.site.register(Camera)
admin.site.register(Foto)
admin.site.register(Prenotazione)
admin.site.register(CalendarioPrenotazione)
admin.site.register(Stagione)
admin.site.register(PrezzoCamera)

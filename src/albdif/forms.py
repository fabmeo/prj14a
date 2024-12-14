import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Prenotazione, CalendarioPrenotazione


class LoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)


class PrenotazioneForm(forms.ModelForm):
    richiesta = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 50}))

    class Meta:
        model = Prenotazione
        #fields = '__all__'
        exclude = ['visitatore', 'camera', 'stato_prenotazione', 'data_prenotazione']


class CalendarioPrenotazioneForm(forms.ModelForm):
    class Meta:
        model = CalendarioPrenotazione
        #fields = '__all__'
        exclude = ['prenotazione']

    def clean(self):
        cleaned_data = super(CalendarioPrenotazioneForm, self).clean()
        di = cleaned_data.get("data_inizio")
        df = cleaned_data.get("data_fine")
        if df < di:
            raise ValidationError("La data fine non può essere antecedente alla data inizio")
        if di <= datetime.datetime.now().date():
            raise ValidationError("La data inizio deve essere futura")
        gia_prenotata = CalendarioPrenotazione.objects.filter(
            Q(prenotazione__camera=self.instance.prenotazione.camera),
            Q(data_fine__gte=di), Q(data_inizio__lte=df),
            ~Q(prenotazione__visitatore=self.instance.prenotazione.visitatore)).count()
        if gia_prenotata > 0:
            raise ValidationError("Spiacenti: la camera è stata già prenotata")
        else:
            return cleaned_data

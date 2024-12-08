from django import forms
from django.contrib.messages import ERROR
from django.core.exceptions import ValidationError

from .models import Prenotazione, CalendarioPrenotazione


class LoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)


class PrenotazioneForm(forms.ModelForm):
    richiesta = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 50}))

    class Meta:
        model = Prenotazione
        fields = '__all__'
        exclude = ['visitatore', 'camera', 'stato_prenotazione', 'data_prenotazione']


class CalendarioPrenotazioneForm(forms.ModelForm):
    class Meta:
        model = CalendarioPrenotazione
        fields = '__all__'
        exclude = ['prenotazione']

    def clean(self):
        cleaned_data = super(CalendarioPrenotazioneForm, self).clean()
        di = cleaned_data.get("data_inizio")
        df = cleaned_data.get("data_fine")
        gia_prenotata = CalendarioPrenotazione.objects.filter(
            prenotazione__camera=self.instance.prenotazione.camera,
            data_fine__gte=di, data_inizio__lte=df).count()
        if gia_prenotata > 0:
            message = "Spiacenti: la camera è stata già prenotata"
            message_level = ERROR
            raise ValidationError(message, params={'value': message_level})
        else:
            return cleaned_data

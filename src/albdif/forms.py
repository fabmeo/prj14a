from django import forms

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
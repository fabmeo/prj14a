from django import forms

from .models import Prenotazione, CalendarioPrenotazione


class LoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)


class PrenotazioneForm(forms.ModelForm):
    class Meta:
        model = Prenotazione
        fields = '__all__'


class CalendarioPrenotazioneForm(forms.ModelForm):
    class Meta:
        model = CalendarioPrenotazione
        fields = '__all__'

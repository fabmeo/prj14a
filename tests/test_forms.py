import datetime
import pytest

from albdif.forms import PrenotazioneForm, CalendarioPrenotazioneForm, LoginForm
from albdif.models import Visitatore, Camera


@pytest.mark.django_db
class TestFormPrenotazione:
    def test_calendario_prenotazione_futura(self, create_utenti, create_visitatori, create_proprieta, create_camere, create_prenotazioni, create_calendario_prenotazioni):
        v = Visitatore.objects.get(utente__id=1)
        c = Camera.objects.get(id=1)
        form_prenotazione_data = {
            'richiesta': "bla bla",
            'data_prenotazione': datetime.date.today()
        }
        form = PrenotazioneForm(data=form_prenotazione_data)
        form.instance.visitatore = v
        form.instance.camera = c
        form.instance.richiesta = "bla bla"
        form.instance.data_prenotazione = datetime.date.today()
        assert form.is_valid(), f"Form errors: {form.errors}"

        form_calendario_data = {
            'data_inizio': datetime.date(2024, 1, 1),
            'data_fine': datetime.date(2024, 1, 10),
        }
        form_cal = CalendarioPrenotazioneForm(data=form_calendario_data)
        assert not form_cal.is_valid(), f"Form errors: {form_cal.errors}"
        assert "La data inizio deve essere futura" in form_cal.errors['__all__']

        form_calendario_data = {
            'data_inizio': datetime.date(2024, 2, 1),
            'data_fine': datetime.date(2024, 1, 10),
        }
        form_cal = CalendarioPrenotazioneForm(data=form_calendario_data)
        assert not form_cal.is_valid(), f"Form errors: {form_cal.errors}"
        assert "La data fine non può essere antecedente alla data inizio" in form_cal.errors['__all__']

        form_calendario_data = {
            'data_inizio': datetime.date(2026, 1, 3),
            'data_fine': datetime.date(2026, 1, 8),
        }
        form_cal = CalendarioPrenotazioneForm(data=form_calendario_data)
        form_cal.instance.prenotazione = form.instance
        assert not form_cal.is_valid(), f"Form errors: {form_cal.errors}"
        assert "Spiacenti: le date si sovrappongono ad un'altra tua prenotazione" in form_cal.errors['__all__']

    def test_calendario_prenotazione_sovrapposizione(self, create_utenti, create_visitatori, create_proprieta, create_camere, create_prenotazioni, create_calendario_prenotazioni):
        v = Visitatore.objects.get(utente__id=2)
        c = Camera.objects.get(id=1)
        form_prenotazione_data = {
            'richiesta': "bla bla",
            'data_prenotazione': datetime.date.today()
        }
        form = PrenotazioneForm(data=form_prenotazione_data)
        form.instance.visitatore = v
        form.instance.camera = c
        form.instance.richiesta = "bla bla"
        form.instance.data_prenotazione = datetime.date.today()
        assert form.is_valid(), f"Form errors: {form.errors}"

        form_calendario_data = {
            'data_inizio': datetime.date(2026, 1, 3),
            'data_fine': datetime.date(2026, 1, 8),
        }
        form_cal = CalendarioPrenotazioneForm(data=form_calendario_data)
        form_cal.instance.prenotazione = form.instance
        assert not form_cal.is_valid(), f"Form errors: {form_cal.errors}"
        assert "Spiacenti: la camera è stata già prenotata" in form_cal.errors['__all__']

    def test_calendario_prenotazione_ok(self, create_utenti, create_visitatori, create_proprieta, create_camere, create_prenotazioni, create_calendario_prenotazioni):
        v = Visitatore.objects.get(utente__id=2)
        c = Camera.objects.get(id=2)
        form_prenotazione_data = {
            'richiesta': "bla bla",
            'data_prenotazione': datetime.date.today()
        }
        form = PrenotazioneForm(data=form_prenotazione_data)
        form.instance.visitatore = v
        form.instance.camera = c
        form.instance.richiesta = "bla bla"
        form.instance.data_prenotazione = datetime.date.today()
        assert form.is_valid(), f"Form errors: {form.errors}"

        form_calendario_data = {
            'data_inizio': datetime.date(2026, 1, 3),
            'data_fine': datetime.date(2026, 1, 8),
        }
        form_cal = CalendarioPrenotazioneForm(data=form_calendario_data)
        form_cal.instance.prenotazione = form.instance
        assert form_cal.is_valid(), f"Form errors: {form_cal.errors}"


import pytest
from django.core.management import call_command
from albdif.models import Proprieta, Camera, Prenotazione, Stagione, CalendarioPrenotazione, RuoloUtente, Visitatore


@pytest.mark.django_db
def test_crea_dati_test():
    import os
    os.chdir('src')
    call_command('crea_dati_test', )
    os.chdir('..')
    
    assert Visitatore.objects.count() == 3
    assert Proprieta.objects.filter(principale=True).count() == 1
    assert RuoloUtente.objects.all().count() == 5
    assert Stagione.objects.count() == 5
    assert Proprieta.objects.count() == 4
    assert Camera.objects.count() == 16
    assert Prenotazione.objects.count() == 35
    assert CalendarioPrenotazione.objects.count() == 35

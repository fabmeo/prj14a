### File presenti nella root del progetto e loro significato

| nome file              | descrizione                                                                                                        |
|------------------------|--------------------------------------------------------------------------------------------------------------------|
| .gitignore             | specifiche su cosa includere/escludere dalle commit                                                                |
| [README.md](README.md) | Specifica come scaricare ed eseguire il progetto                                                                   |
| compose.yaml           | Istruzioni per eseguire il progetto mediante "docker-compose"                                                      |
| pyproject.toml         | file che definisce le librerie che il progetto include e che saranno installate nel virtualenv                     |
| pytest.ini             | file di settings della libreria pytest                                                                             |
| uv.lock                | file creato con il comando "uv sync" che "blocca" le versioni delle librerie che saranno installate nel virtualenv |

===

### Struttura del progetto

```
<pre>
src
├───albdif
│   ├───config - impostazioni di progetto
│   │       (include i valori di default delle variabili d'ambiente) 
│   ├───management
│   │   ├───commands - comandi di progetto
│   │   │   (include il file per creare i dati fittizi di prova)
│   │   
│   ├───migrations - istruzioni per la creazione del database
│   │   
│   ├───templates - le pagine HTML (pensando al pattern MVC che in Django è MVT è il Template -> interfaccia utente)
│   │   └───albdif
│   │       └───include - porzioni di HTML incluse in più pagine
│   ├───utils - funzioni e/o classi di servizio
│   │       (presente il file "fixtures.py" necessario per creare i dati di test)
│   │       (presente il file "pipeline.py" necessario per la creazione automatica dell'utente da Github, Google, etc.) 
│   │       (presente il file "utility.py" che contiene funzioni di utilità comuni)
│   admin.py - è il file con cui si configura la dashboard del sito di amministrazione Django
│   forms.py - è il modulo che si occupa dei controlli di validazione sui dati inseriti nei form dall'utente
│   models.py - è il modulo che pilota l'ORM di Django (il Model del pattern MVT di Django)
│   urls.py - è il file che associa la url alla views da eseguire
│   views.py - è il modulo in cui è specificata la logica di business (il Controller nel pattern MVT di Django)
└───static - contiene i file statici (css, javascript e immagini)
    ├───css - contiene il file css di progetto
    ├───img - contiene le immagini demo utilizzate nel progetto quando eseguito con i dati di prova
    │   └───site - contiene il file favicon.png
    └───js - contiene i javascript utilizzati nelle pagine html

tests - contiene i moduli di test
│   .coveragerc - impostazioni per il calcolo della copertura del codice dai test (include la soglia sotto la quale la action Github fallisce)
│   conftest.py - imposta l'applicazione Django per i test per un utente fittizio e disabilita i controlli CSRF
│   test_commands.py - testa il modulo command
│   test_models.py - testa il modulo models
│   test_pipeline.py - testa la pipeline per l'autenticazione integrata con github 
│   test_utility.py - testa il modulo utility
│   test_views.py - testa il modulo views

</pre>
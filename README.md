# Benvenuti nel progetto PW14A

Titolo: **Albergo Diffuso Pegasus**

Autore: fabio meoli

---
### Prerequisiti per l'avvio del progetto in locale (SO Windows)
1. installazione di python versione 3.12 (https://www.python.org/downloads/windows/)  
2. installazione di uv (https://docs.astral.sh/uv/getting-started/installation/)
> pip install uv


Per provare il progetto:

1. copia del codice dal repository Github
> git clone https://github.com/fabmeo/prj14a.git
2. accedere alla directory pw14a
> cd pw14a
3. installazione del virtualenv
> uv sync
> - alla fine dell'installazione il virtualenv si attiva automaticamente e il prompt è come segue:
> - (pw14a) C:\prj\pw14a>
3. verifica del progetto con l'esecuzione dei test
> pytest tests

4. impostazione delle variabili d'ambiente
> **NCESSARIE**
> ```
> set PEGASUS_MEDIA_URL=media/
> set PEGASUS_MEDIA_ROOT=c:/prj/pw14a/media/
> set PEGASUS_DATABASE_URL=sqlite:///C:/prj/pw14a/database/db.sqlite3
> set PEGASUS_SOCIAL_AUTH_REDIRECT_IS_HTTPS=0
> ```
> **OPZIONALI**
> ```
> set PEGASUS_SOCIAL_AUTH_GITHUB_KEY=<inserire la api key github>
> set PEGASUS_SOCIAL_AUTH_GITHUB_SECRET=<inserire la secret key github>
> set PEGASUS_SOCIAL_AUTH_GITHUB_REDIRECT_URI=http://localhost:8000/social/complete/github/
> ```
5. creazione del database (accesso alla sotto-directory src)
> cd src
> python manage.py migrate
6. creazione dei dati di test (include utente "guest")
> python manage.py crea_dati_test
7. avvio del server
> python manage.py runserver localhost:8000
8. Click sulla url del sito in esecuzione (vedi sotto)
> System check identified 3 issues (0 silenced).
> January 01, 2025 - 21:04:58
> Django version 4.2.17, using settings 'albdif.config.settings'
> Starting development server at http://localhost:8000/
> Quit the server with CTRL-BREAK.
9. Il sito è navigabile in modalità anonima ma può essere acceduto anche con le seguenti credenziali:
> utente: **guest**
> password: **password**

---

## COMANDI DI UTILITA'

1. Dati di test
> python manage.py dumpdata > albdif\fixtures\albdif_new

---

## COME AVVIARE IL SERVER

1. avviare il virtualenv
> .venv\scripts\activate
2. Dalla directory: (pw14a-3.12) C:\prj\pw14a digitare il comando sotto
> python manage.py runserver

VARIABILI AMBIENTE DA IMPOSTARE:
- export PEGASUS_MEDIA_URL='media/'
- export PEGASUS_MEDIA_ROOT='c:/prj/pw14a/media/'
- export PEGASUS_DATABASE_URL='sqlite:///C:/prj/pw14a/src/db.sqlite3'

## AVVIARE I TEST

1. avviare il virtualenv
> .venv\scripts\activate
2. Dalla directory: (pw14a-3.13) C:\prj\pw14a digitare il comando sotto
> pytest tests
3. test con il coverage
> pytest -vvv -s --disable-warnings --cov-report=html --cov=src/albdif tests

---

## DOCKER

Comandi di utilità

Prima di codificare lo yaml
> docker build -t pw14a .

> docker run -p 8080:8000 pw14a

> docker run --env-file .envdkc -p 8080:8000 pw14a

Dopo la codifica dello yaml
> docker-compose up --build -d
> docker-compose --env-file .envdkc up --build -d

bash
docker stop <container_id>
docker run -d -p 8080:8080 hello-world-go
docker exec -it <container_id> bash

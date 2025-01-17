# Benvenuti, in questa pagina trovate le informazioni per scaricare ed eseguire il progetto 

Titolo: **Albergo Diffuso Pegasus**

---
### Prerequisiti per l'avvio del progetto in locale (SO Windows)
1. installazione di python versione 3.12 (https://www.python.org/downloads/windows/)  
2. installazione di uv (https://docs.astral.sh/uv/getting-started/installation/)
> pip install uv
3. clone del codice dal repository Github 
> posizionarsi su una directory: es c:\prj ed eseguire il comando seguente
> git clone https://github.com/fabmeo/prj14a.git
4. accedere alla directory pw14a
> cd pw14a
5. sono presenti le seguenti due opzioni: 

   * [Esecuzione del progetto in locale](#esecuzione-del-progetto-in-locale)
   * [Esecuzione del progetto con Docker](#esecuzione-del-progetto-con-docker)

### Esecuzione del progetto in locale
1. installazione del virtualenv
> uv sync
> - alla fine dell'installazione il virtualenv si attiva automaticamente e il prompt è come segue:
> - (pw14a) C:\prj\pw14a>
2. verifica del progetto con l'esecuzione dei test
> pytest tests
3. impostazione delle variabili d'ambiente
> **NECESSARIE**
> ```
> set PEGASUS_MEDIA_URL=media/
> set PEGASUS_MEDIA_ROOT=c:/prj/pw14a/media/
> set PEGASUS_DATABASE_URL=sqlite:///C:/prj/pw14a/database/db.sqlite3
> set PEGASUS_SOCIAL_AUTH_REDIRECT_IS_HTTPS=0
> set PEGASUS_STATIC_ROOT=C:/prj/pw14a/src/static
> ```
> **OPZIONALI**
> ```
> a) Se si vuole attivare il SSO Github seguire la guida a questo link: https://python-social-auth.readthedocs.io/en/latest/backends/github.html
> b) e registrare una nuova app dalle impostazioni dello sviluppatore del proprio account Github: https://github.com/settings/applications/new 
> c) Questo permetterà di ottenere la coppia key/secret da imposare di seguito e consentire la registrazione immediata dell'account sull'applicazione AD Pegasus 
> set PEGASUS_SOCIAL_AUTH_GITHUB_KEY=<inserire la api key github>
> set PEGASUS_SOCIAL_AUTH_GITHUB_SECRET=<inserire la secret key github>
> set PEGASUS_SOCIAL_AUTH_GITHUB_REDIRECT_URI=http://localhost:8000/social/complete/github/
> ```
4. creazione del database (accesso alla sotto-directory src)
> ```
> cd src
> python manage.py migrate
> ```
5. creazione dei dati di test (include utente "guest" per navigare il sito come un utente già registrato e l'utente "admin" per accedere all'Admin Site)
> python manage.py crea_dati_test
6. avvio del server
> python manage.py runserver localhost:8000
7. Click sulla url del sito in esecuzione come nell'esempio sottostante
> ```
> <esempio della shell come si dovrebbe vedere con il server online> 
> ...
> System check identified 3 issues (0 silenced).
> January 01, 2025 - 21:04:58
> Django version 4.2.17, using settings 'albdif.config.settings'
> Starting development server at http://localhost:8000/
> Quit the server with CTRL-BREAK.
> ```
8. Il sito è navigabile in modalità anonima ma può essere acceduto anche con le seguenti credenziali:
> utente: **guest**
> password: **password**

---

### Esecuzione del progetto con DOCKER

Con questa configurazione si crea una composizione con due servizi: **web** e **postgres** 

### Prerequisiti: DockerDesktop installato sul proprio SO: (https://www.docker.com/products/docker-desktop/)

1. dalla directory del progetto (es c:\prj\pw14a) lanciare il comando che segue
> docker compose up
2. aprire una finestra sul browser e incollare la seguente url
> http://localhost:8000
3. Il sito è navigabile in modalità anonima ma può essere acceduto anche con le seguenti credenziali:
> utente: **guest**
> password: **password**
4. il sito di amministrazione può essere acceduto dalla seguente url: http://localhost:8000/admin  
> utente: **admin**
> password: **password**

---

### Per avere invece un'idea di come è stato strutturato il progetto

[Struttura del progetto](docs/Partecipa.md)


## COMANDI DI UTILITA'

1. Dump dei dati sul database
> python manage.py dumpdata > albdif\fixtures\albdif_new

---

## AVVIARE IL SERVER

1. avviare il virtualenv
> .venv\scripts\activate
2. Dalla directory: (pw14a-3.12) C:\prj\pw14a digitare il comando sotto
> python manage.py runserver

VARIABILI AMBIENTE DA IMPOSTARE:
- export PEGASUS_MEDIA_URL='media/'
- export PEGASUS_MEDIA_ROOT='c:/prj/pw14a/media/'
- export PEGASUS_DATABASE_URL='sqlite:///C:/prj/pw14a/src/db.sqlite3'

---

## AVVIARE I TEST

1. avviare il virtualenv
> .venv\scripts\activate
2. Dalla directory: (pw14a-3.13) C:\prj\pw14a digitare il comando sotto
> pytest tests
3. test con il coverage
> pytest tests

---

## DOCKER

Creazione dell'immagine:
> docker build -t pw14a .

Esecuzione del container:
> docker run -p 8080:8000 pw14a 

Altri comandi di utilità
> ``` 
> docker ps -a
> docker stop <container_id>
> docker exec -it <container_id> bash
> ```

---

## DOCKER COMPOSE

> docker-compose up --build -d


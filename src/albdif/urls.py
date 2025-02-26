from django.urls import path
from . import views

app_name = "albdif"
urlpatterns = [
    path("", views.home, name="home"),
    # ex: /login/
    path("login/", views.login.as_view(), name="login"),
    # ex: /logout/
    path("logout/", views.logout.as_view(), name="logout"),
    # ex: /profilo/1/
    path("profilo/<int:pk>/", views.profilo.as_view(), name="profilo"),
    # ex: /registrazione/
    path("registrazione/", views.registrazione.as_view(), name="registrazione"),
    # ex: /registrazione_titolare/
    path("registrazione_titolare/", views.registrazione_titolare.as_view(), name="registrazione_titolare"),
    # ex: /contatti/
    path("contatti/", views.contatti.as_view(), name="contatti"),

    # ex: /partner/   -> le proprietà dei partener
    path("partner/", views.proprieta_partner.as_view(), name="proprieta_partner"),
    # ex: /proprieta/1/
    path("proprieta/<int:pk>/", views.proprieta_detail.as_view(), name="proprieta_detail"),

    # ex: /camere/     -> solo quelle dell'AD principale
    path("camere/", views.camere_list.as_view(), name="camere_list"),
    # ex: /camera/1/
    path("camera/<int:pk>/", views.camera_detail.as_view(), name="camera_detail"),
    # ex: /prenota_camera/1/2/
    path("prenota_nuova/<int:id1>/<int:id2>/", views.prenota_camera.as_view(), name="prenota_camera"),
    # ex: /prenota_modifica/1/
    path("prenota_modifica/<int:id1>/", views.prenota_modifica.as_view(), name="prenota_modifica"),
    # ex: /prenota_cancella/1/
    path("prenota_cancella/<int:id1>/", views.prenota_cancella.as_view(), name="prenota_cancella"),
    # ex: /prenota_paga/1/
    path("prenota_paga/<int:id1>/", views.prenota_paga.as_view(), name="prenota_paga"),

    # ex: /prezzi_camera/
    path("prezzi_camera/", views.prezzi_camera_list.as_view(), name="prezzi_camera_list"),
    # ex: /prezzo_camera/1/
    path("prezzo_camera/<int:pk>/", views.prezzo_camera_detail.as_view(), name="prezzo_camera_detail"),

]

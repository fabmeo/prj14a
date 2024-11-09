from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # ex: /stagioni/
    path("stagioni/", views.stagioni_list, name="stagioni_list"),
    # ex: /stagione/5/
    path("stagione/<int:stagione_id>/", views.stagione_detail, name="stagione_detail"),

    # ex: /proprieta/
    path("proprieta/", views.proprieta_list, name="proprieta_list"),
    # ex: /proprieta/1/
    path("proprieta/<int:proprieta_id>/", views.proprieta_detail, name="proprieta_detail"),

    # ex: /camere/
    path("camere/", views.camere_list, name="camere_list"),
    # ex: /camera/1/
    path("camera/<int:camera_id>/", views.camera_detail, name="camera_detail"),

    # ex: /prenotazioni/
    path("prenotazioni/", views.prenotazioni_list, name="prenotazioni_list"),
    # ex: /prenotazione/1/
    path("prenotazione/<int:prenotazione_id>/", views.prenotazione_detail, name="prenotazione_detail"),

]

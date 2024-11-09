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

    # ex: /prezzi_camera/
    path("prezzi_camera/", views.prezzi_camera_list, name="prezzi_camera_list"),
    # ex: /prezzo_camera/1/
    path("prezzo_camera/<int:prezzocamera_id>/", views.prezzo_camera_detail, name="prezzo_camera_detail"),

    # ex: /prenotazioni/
    path("prenotazioni/", views.prenotazioni_list, name="prenotazioni_list"),
    # ex: /prenotazione/1/
    path("prenotazione/<int:prenotazione_id>/", views.prenotazione_detail, name="prenotazione_detail"),

    # ex: /calendario_prenotazioni/
    path("calendario_prenotazioni/", views.calendario_prenotazioni_list, name="calendario_prenotazioni_list"),
    # ex: /calendario_prenotazione/1/
    path("calendario_prenotazione/<int:calendario_prenotazione_id>/", views.calendario_prenotazione_detail, name="calendario_prenotazione_detail"),

    path('calendar/', views.calendario_camera, name='calendar'),
]

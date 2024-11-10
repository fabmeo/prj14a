from django.urls import path

from . import views

app_name = "albdif"
urlpatterns = [
    path("", views.home, name="index"),

    # ex: /stagioni/
    path("stagioni/", views.stagioni_list.as_view(), name="stagioni_list"),
    # ex: /stagione/5/
    path("stagione/<int:pk>/", views.stagione_detail.as_view(), name="stagione_detail"),

    # ex: /proprieta/
    path("proprieta/", views.proprieta_list.as_view(), name="proprieta_list"),
    # ex: /proprieta/1/
    path("proprieta/<int:pk>/", views.proprieta_detail.as_view(), name="proprieta_detail"),

    # ex: /camere/
    path("camere/", views.camere_list.as_view(), name="camere_list"),
    # ex: /camera/1/
    path("camera/<int:pk>/", views.camera_detail.as_view(), name="camera_detail"),

    # ex: /prezzi_camera/
    path("prezzi_camera/", views.prezzi_camera_list.as_view(), name="prezzi_camera_list"),
    # ex: /prezzo_camera/1/
    path("prezzo_camera/<int:pk>/", views.prezzo_camera_detail.as_view(), name="prezzo_camera_detail"),

    # ex: /prenotazioni/
    path("prenotazioni/", views.prenotazioni_list, name="prenotazioni_list"),
    # ex: /prenotazione/1/
    path("prenotazione/<int:prenotazione_id>/", views.prenotazione_detail, name="prenotazione_detail"),

    # ex: /calendario_prenotazioni/
    path("calendario_prenotazioni/", views.calendario_prenotazioni_list, name="calendario_prenotazioni_list"),
    # ex: /calendario_prenotazione/1/
    path("calendario_prenotazione/<int:calendario_prenotazione_id>/", views.calendario_prenotazione_detail, name="calendario_prenotazione_detail"),

    path('calendario_camera/', views.calendario_camera, name='calendario_camera'),
]

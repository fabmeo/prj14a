from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # ex: /prop/5/
    path("proprieta/<int:proprieta_id>/", views.proprieta_detail, name="prop_detail"),
    # ex: /prop/5/camera/
    path("camera/<int:camera_id>/", views.camera_detail, name="camera_detail"),
]

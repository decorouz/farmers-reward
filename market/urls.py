from django.urls import path

from . import views

urlpatterns = [
    path("farmers/", views.index, name="index"),
]

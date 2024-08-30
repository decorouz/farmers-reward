from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path("", views.contact_us, name="contact_form"),
    path(
        "thanks/",
        lambda request: render(request, "contact_us/thanks.html"),
        name="contact_thanks",
    ),
]

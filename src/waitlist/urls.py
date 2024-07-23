from django.urls import path

from . import views

urlpatterns = [
    path("join/", views.join_waitlist, name="join_waitlist"),
    path("success/", views.waitlist_success, name="waitlist_success"),
]

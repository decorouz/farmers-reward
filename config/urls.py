from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("market", include("market.urls")),
    path("farmers/", include("farmers.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]

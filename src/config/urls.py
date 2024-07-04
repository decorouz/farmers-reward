from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("market", include("market.urls")),
    path("farmers/", include("farmers.urls")),
    path("subsidy/", include("subsidy.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]

# if settings.DEBUG:
#     # do not do this in prod
#     from django.conf.urls.static import static

#     # Try Django
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

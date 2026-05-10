"""standarcloud URL configuration."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from standarcloud.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    # Auth
    path("accounts/", include("standarcloud.apps.accounts.urls")),
    # Web UI
    path("", include("standarcloud.apps.projects.urls")),
    path("assets/", include("standarcloud.apps.assets.urls")),
    path("tokens/", include("standarcloud.apps.tokens.urls")),
    path("", include("standarcloud.apps.memory.urls")),
    # REST API v1
    path("api/v1/", include("standarcloud.apps.api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

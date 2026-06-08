"""
URL Configuration — Task API
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # ── Admin ────────────────────────────────────────────
    path("admin/", admin.site.urls),

    # ── API v1 ───────────────────────────────────────────
    path("api/auth/", include("apps.users.urls.auth_urls")),
    path("api/users/", include("apps.users.urls.user_urls")),
    path("api/tasks/", include("apps.tasks.urls")),

    # ── Schema & Docs ────────────────────────────────────
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

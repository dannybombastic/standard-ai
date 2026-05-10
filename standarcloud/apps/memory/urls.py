"""URLs for memory UI (sessions + entries)."""

from django.urls import path

from .views import ProjectSessionDetailView, ProjectSessionListView

app_name = "memory"

urlpatterns = [
    path("projects/<slug:slug>/memory/", ProjectSessionListView.as_view(), name="project_sessions"),
    path(
        "projects/<slug:slug>/memory/<uuid:session_id>/",
        ProjectSessionDetailView.as_view(),
        name="project_session_detail",
    ),
]

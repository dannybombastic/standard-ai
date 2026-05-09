"""Assets URL configuration."""
from django.urls import path
from . import views

app_name = "assets"

urlpatterns = [
    path("<slug:project_slug>/", views.AssetListView.as_view(), name="list"),
    path("<slug:project_slug>/new/", views.AssetCreateView.as_view(), name="create"),
    path("<slug:project_slug>/new/<str:asset_type>/", views.AssetCreateView.as_view(), name="create_typed"),
    path("<slug:project_slug>/<uuid:pk>/", views.AssetDetailView.as_view(), name="detail"),
    path("<slug:project_slug>/<uuid:pk>/edit/", views.AssetUpdateView.as_view(), name="update"),
    path("<slug:project_slug>/<uuid:pk>/delete/", views.AssetDeleteView.as_view(), name="delete"),
]

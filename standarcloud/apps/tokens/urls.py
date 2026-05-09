"""Tokens URL configuration."""
from django.urls import path
from . import views

app_name = "tokens"

urlpatterns = [
    path("", views.TokenListView.as_view(), name="list"),
    path("new/", views.TokenCreateView.as_view(), name="create"),
    path("<uuid:pk>/delete/", views.TokenDeleteView.as_view(), name="delete"),
]

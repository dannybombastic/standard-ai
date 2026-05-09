"""Root views for StandarCloud."""
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class HomeView(LoginRequiredMixin, TemplateView):
    """Landing page shown to authenticated users. Redirects to login otherwise."""

    template_name = "home.html"
    login_url = "/accounts/login/"

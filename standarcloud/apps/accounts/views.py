"""Account views — login, logout, register, profile."""
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, RedirectView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages


class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url:
            from django.shortcuts import redirect
            return redirect(next_url)
        return super().form_valid(form)


class LogoutView(RedirectView):
    url = reverse_lazy("accounts:login")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Account created successfully.")
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

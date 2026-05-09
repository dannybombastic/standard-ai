"""Token management views."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import ApiToken
from .forms import ApiTokenCreateForm


class TokenListView(LoginRequiredMixin, ListView):
    model = ApiToken
    template_name = "tokens/list.html"
    context_object_name = "tokens"

    def get_queryset(self):
        return ApiToken.objects.filter(user=self.request.user)


class TokenCreateView(LoginRequiredMixin, CreateView):
    model = ApiToken
    template_name = "tokens/create.html"
    form_class = ApiTokenCreateForm
    success_url = reverse_lazy("tokens:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Token created. Copy it now — it won't be shown again: {self.object.token}",
        )
        return response


class TokenDeleteView(LoginRequiredMixin, DeleteView):
    model = ApiToken
    template_name = "tokens/confirm_delete.html"
    success_url = reverse_lazy("tokens:list")

    def get_queryset(self):
        return ApiToken.objects.filter(user=self.request.user)

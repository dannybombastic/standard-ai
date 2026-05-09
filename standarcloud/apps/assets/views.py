"""Asset views."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from standarcloud.apps.projects.models import Project
from .models import Asset
from .forms import AssetForm, AssetQuickCreateForm


class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = "assets/list.html"
    context_object_name = "assets"

    def get_queryset(self):
        self.project = get_object_or_404(
            Project, slug=self.kwargs["project_slug"], owner=self.request.user
        )
        return Asset.objects.filter(project=self.project)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["project"] = self.project
        return ctx


class AssetDetailView(LoginRequiredMixin, DetailView):
    model = Asset
    template_name = "assets/detail.html"
    context_object_name = "asset"

    def get_queryset(self):
        return Asset.objects.filter(project__owner=self.request.user)


class AssetCreateView(LoginRequiredMixin, CreateView):
    model = Asset
    template_name = "assets/form.html"
    form_class = AssetForm

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(
            Project, slug=self.kwargs["project_slug"], owner=self.request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        asset_type = self.kwargs.get("asset_type")
        if asset_type:
            # Force type via disabled field in the form
            return lambda *a, **k: AssetQuickCreateForm(*a, forced_type=asset_type, **k)
        return AssetForm

    def form_valid(self, form):
        form.instance.project = self.project
        # Ensure forced type is applied even if field is disabled
        asset_type = self.kwargs.get("asset_type")
        if asset_type:
            form.instance.asset_type = asset_type
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("assets:detail", kwargs={"project_slug": self.project.slug, "pk": self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["project"] = self.project
        ctx["is_create"] = True
        ctx["forced_type"] = self.kwargs.get("asset_type")
        return ctx


class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    template_name = "assets/form.html"
    form_class = AssetForm

    def get_queryset(self):
        return Asset.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy("assets:detail", kwargs={"project_slug": self.object.project.slug, "pk": self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["project"] = self.object.project
        ctx["is_create"] = False
        return ctx


class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    template_name = "assets/confirm_delete.html"

    def get_queryset(self):
        return Asset.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            "assets:list",
            kwargs={"project_slug": self.object.project.slug},
        )

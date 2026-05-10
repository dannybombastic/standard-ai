"""Project views."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.text import slugify

from .models import Project, ProjectConfig


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/detail.html"
    context_object_name = "project"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["assets"] = self.object.assets.all().order_by("asset_type", "name")
        return ctx


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = "projects/form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("projects:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.slug = slugify(form.instance.name)
        response = super().form_valid(form)
        # Create default config
        ProjectConfig.objects.create(project=self.object)
        return response


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = "projects/form.html"
    fields = ["name", "description"]
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy("projects:detail", kwargs={"slug": self.object.slug})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/confirm_delete.html"
    success_url = reverse_lazy("projects:list")
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

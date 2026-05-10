"""Frontend views for session memory (Session + MemoryEntry)."""

from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from standarcloud.apps.projects.models import Project
from .models import Session, MemoryEntry


class ProjectSessionListView(LoginRequiredMixin, ListView):
    """List sessions for a given project (owner-scoped)."""

    model = Session
    template_name = "memory/session_list.html"
    context_object_name = "sessions"
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, owner=request.user, slug=kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (
            Session.objects.filter(project=self.project, user=self.request.user)
            .order_by("-last_activity_at", "-started_at")
            .select_related("project", "user")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["project"] = self.project
        return ctx


class ProjectSessionDetailView(LoginRequiredMixin, DetailView):
    """Show one session and its memory entries."""

    model = Session
    template_name = "memory/session_detail.html"
    context_object_name = "session"
    pk_url_kwarg = "session_id"

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, owner=request.user, slug=kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Session.objects.filter(project=self.project, user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        session: Session = ctx["session"]
        ctx["project"] = self.project
        ctx["entries"] = (
            MemoryEntry.objects.filter(session=session)
            .order_by("-created_at")
            .select_related("session", "session__project")
        )
        return ctx

"""Project models."""
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    """A standarcloud project owned by a user."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


class ProjectConfig(models.Model):
    """Key-value configuration entries for a project."""

    VISIBILITY_PUBLIC = "public"
    VISIBILITY_PRIVATE = "private"
    VISIBILITY_CHOICES = [
        (VISIBILITY_PUBLIC, "Public"),
        (VISIBILITY_PRIVATE, "Private"),
    ]

    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, related_name="config"
    )
    visibility = models.CharField(
        max_length=10, choices=VISIBILITY_CHOICES, default=VISIBILITY_PRIVATE
    )
    extra = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return f"Config({self.project.name})"

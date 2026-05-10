"""Session memory models — structured notes produced by MCP sessions."""
import uuid
from django.conf import settings
from django.db import models

from standarcloud.apps.projects.models import Project


class Session(models.Model):
    """
    Represents a logical MCP session (conversation/run) scoped to a Project + User.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sessions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mcp_sessions")

    title = models.CharField(max_length=255, blank=True, default="")
    external_id = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Optional session id from MCP/client (e.g. conversation id).",
    )

    started_at = models.DateTimeField(auto_now_add=True)
    last_activity_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_activity_at"]
        indexes = [
            models.Index(fields=["project", "user", "-last_activity_at"]),
            models.Index(fields=["external_id"]),
        ]

    def __str__(self) -> str:
        label = self.title or self.external_id or str(self.id)
        return f"{self.project.slug} - {self.user} - {label}"


class MemoryEntry(models.Model):
    """A tagged memory record within a Session."""

    TAG_OBSERVATION = "observation"
    TAG_RECOMMENDATION = "recommendation"
    TAG_DECISION = "decision"
    TAG_ARCHITECTURE = "architecture"
    TAG_OTHER = "other"

    TAG_CHOICES = [
        (TAG_OBSERVATION, "Observation"),
        (TAG_RECOMMENDATION, "Recommendation"),
        (TAG_DECISION, "Decision"),
        (TAG_ARCHITECTURE, "Architecture"),
        (TAG_OTHER, "Other"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="entries")
    tag = models.CharField(max_length=32, choices=TAG_CHOICES, default=TAG_OTHER)

    title = models.CharField(max_length=255, blank=True, default="")
    content = models.TextField()

    # Optional structured data for future extensions (e.g. metadata, links, file refs)
    metadata = models.JSONField(blank=True, default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["session", "created_at"]),
            models.Index(fields=["tag", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.tag}: {self.title or self.id}"

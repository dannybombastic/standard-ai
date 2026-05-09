"""API Token models."""
import secrets
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def _generate_token() -> str:
    return secrets.token_urlsafe(32)


class ApiToken(models.Model):
    """Personal API token for MCP server authentication."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_tokens")
    name = models.CharField(max_length=100, help_text="Human-readable label")
    token = models.CharField(max_length=64, unique=True, default=_generate_token)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.user.username})"

    def mask(self) -> str:
        """Return a masked version of the token for display."""
        return f"{self.token[:8]}{'*' * 24}"

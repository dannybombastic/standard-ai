"""Asset models — stores files/templates synced to projects."""
import uuid
from django.db import models
from standarcloud.apps.projects.models import Project


class Asset(models.Model):
    """A file asset belonging to a project (skill, prompt, spec, etc.)."""

    TYPE_SKILL = "skill"
    TYPE_AGENT = "agent"
    TYPE_PROMPT = "prompt"
    TYPE_SPEC = "spec"
    TYPE_OTHER = "other"
    TYPE_CHOICES = [
        (TYPE_SKILL, "Skill"),
        (TYPE_AGENT, "Agent"),
        (TYPE_PROMPT, "Prompt"),
        (TYPE_SPEC, "Spec"),
        (TYPE_OTHER, "Other"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="assets")
    name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_OTHER)
    path = models.CharField(max_length=512, help_text="Relative path within the project")
    content = models.TextField(blank=True)
    content_hash = models.CharField(max_length=64, blank=True)
    size_bytes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["asset_type", "name"]
        unique_together = [("project", "path")]

    def __str__(self) -> str:
        return f"{self.project.name}/{self.path}"


class SkillAsset(Asset):
    """Proxy model for Skill assets — shown as a dedicated section in admin."""

    class Meta:
        proxy = True
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def save(self, *args, **kwargs):
        self.asset_type = Asset.TYPE_SKILL
        super().save(*args, **kwargs)


class PromptAsset(Asset):
    """Proxy model for Prompt assets — shown as a dedicated section in admin."""

    class Meta:
        proxy = True
        verbose_name = "Prompt"
        verbose_name_plural = "Prompts"

    def save(self, *args, **kwargs):
        self.asset_type = Asset.TYPE_PROMPT
        super().save(*args, **kwargs)


class AgentAsset(Asset):
    """Proxy model for Agent assets — shown as a dedicated section in admin."""

    class Meta:
        proxy = True
        verbose_name = "Agent"
        verbose_name_plural = "Agents"

    def save(self, *args, **kwargs):
        self.asset_type = Asset.TYPE_AGENT
        super().save(*args, **kwargs)


class SpecAsset(Asset):
    """Proxy model for Spec assets — shown as a dedicated section in admin."""

    class Meta:
        proxy = True
        verbose_name = "Spec"
        verbose_name_plural = "Specs"

    def save(self, *args, **kwargs):
        self.asset_type = Asset.TYPE_SPEC
        super().save(*args, **kwargs)


class OtherAsset(Asset):
    """Proxy model for Other assets — shown as a dedicated section in admin."""

    class Meta:
        proxy = True
        verbose_name = "Other Asset"
        verbose_name_plural = "Other Assets"

    def save(self, *args, **kwargs):
        self.asset_type = Asset.TYPE_OTHER
        super().save(*args, **kwargs)

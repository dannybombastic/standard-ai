"""DRF serializers for session memory (Session + MemoryEntry)."""
from rest_framework import serializers

from standarcloud.apps.memory.models import Session, MemoryEntry
from standarcloud.apps.projects.models import Project


class SessionSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(slug_field="slug", queryset=Project.objects.none())
    entry_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Session
        fields = [
            "id",
            "project",
            "title",
            "external_id",
            "started_at",
            "last_activity_at",
            "entry_count",
        ]
        read_only_fields = ["id", "started_at", "last_activity_at", "entry_count"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["project"].queryset = Project.objects.filter(owner=request.user)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class MemoryEntrySerializer(serializers.ModelSerializer):
    session_id = serializers.UUIDField(write_only=True, required=False)
    session = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MemoryEntry
        fields = [
            "id",
            "session",
            "session_id",
            "tag",
            "title",
            "content",
            "metadata",
            "created_at",
        ]
        read_only_fields = ["id", "session", "created_at"]

"""DRF serializers for all StandarCloud models."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from standarcloud.apps.projects.models import Project
from standarcloud.apps.tokens.models import ApiToken
from standarcloud.apps.assets.models import Asset

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]
        read_only_fields = fields


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    asset_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "owner",
            "asset_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "owner", "asset_count", "created_at", "updated_at"]

    def get_asset_count(self, obj):
        return obj.assets.count()

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class APITokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = ApiToken
        fields = ["id", "name", "token", "created_at", "last_used_at", "expires_at", "is_active"]
        read_only_fields = ["id", "token", "created_at", "last_used_at"]

    def get_token(self, obj):
        return obj.mask()


class APITokenCreateSerializer(serializers.ModelSerializer):
    """Used only on creation — returns the raw token once."""
    token = serializers.CharField(read_only=True)

    class Meta:
        model = ApiToken
        fields = ["id", "name", "token", "created_at"]
        read_only_fields = ["id", "token", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return ApiToken.objects.create(**validated_data)


class AssetSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Project.objects.none(),
    )

    class Meta:
        model = Asset
        fields = [
            "id",
            "project",
            "asset_type",
            "name",
            "path",
            "content",
            "content_hash",
            "size_bytes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "content_hash", "size_bytes", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["project"].queryset = Project.objects.filter(owner=request.user)

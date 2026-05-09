"""DRF ViewSets for StandarCloud API."""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from standarcloud.apps.projects.models import Project
from standarcloud.apps.tokens.models import ApiToken
from standarcloud.apps.assets.models import Asset
from standarcloud.apps.tokens.authentication import ApiTokenAuthentication
from .serializers import (
    ProjectSerializer,
    APITokenSerializer,
    APITokenCreateSerializer,
    AssetSerializer,
)


class IsOwner(permissions.BasePermission):
    """Object-level permission: only the owner can access."""

    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, "owner", None) or getattr(obj, "user", None)
        return owner == request.user


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    authentication_classes = [ApiTokenAuthentication]
    lookup_field = "slug"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class APITokenViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    authentication_classes = [ApiTokenAuthentication]

    def get_queryset(self):
        return ApiToken.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return APITokenCreateSerializer
        return APITokenSerializer

    @action(detail=True, methods=["post"])
    def revoke(self, request, pk=None):
        token = self.get_object()
        token.is_active = False
        token.save(update_fields=["is_active"])
        return Response({"status": "revoked"})


class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [ApiTokenAuthentication]

    def get_queryset(self):
        qs = Asset.objects.filter(project__owner=self.request.user)
        project_slug = self.request.query_params.get("project")
        if project_slug:
            qs = qs.filter(project__slug=project_slug)
        asset_type = self.request.query_params.get("type")
        if asset_type:
            qs = qs.filter(asset_type=asset_type)
        return qs

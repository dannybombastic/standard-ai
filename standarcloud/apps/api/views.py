"""DRF ViewSets for StandarCloud API."""
from django.db.models import Count
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from standarcloud.apps.projects.models import Project
from standarcloud.apps.tokens.models import ApiToken
from standarcloud.apps.assets.models import Asset
from standarcloud.apps.memory.models import Session, MemoryEntry
from standarcloud.apps.tokens.authentication import ApiTokenAuthentication
from .serializers import (
    ProjectSerializer,
    APITokenSerializer,
    APITokenCreateSerializer,
    AssetSerializer,
)
from .memory_serializers import SessionSerializer, MemoryEntrySerializer


class IsOwner(permissions.BasePermission):
    """Object-level permission: only the owner can access.

    Supports common owner fields (`owner`, `user`) and also objects that are owned
    indirectly via a related Project (e.g. Asset -> project -> owner).
    """

    def has_object_permission(self, request, view, obj):
        # Direct ownership
        owner = getattr(obj, "owner", None) or getattr(obj, "user", None)
        if owner is not None:
            return owner == request.user

        # Indirect ownership through a related project (Asset, etc.)
        project = getattr(obj, "project", None)
        if project is not None:
            project_owner = getattr(project, "owner", None)
            return project_owner == request.user

        return False


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
    # Reforzamos permisos: IsOwner aplica object-level permission (definida arriba)
    # y get_queryset limita exposición a assets de proyectos del usuario.
    permission_classes = [permissions.IsAuthenticated, IsOwner]
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


class SessionViewSet(viewsets.ModelViewSet):
    """
    MCP sessions, scoped to the authenticated user.
    """
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [ApiTokenAuthentication]

    def get_queryset(self):
        qs = (
            Session.objects.filter(user=self.request.user)
            .select_related("project")
            .annotate(entry_count=Count("entries"))
        )
        project_slug = self.request.query_params.get("project")
        if project_slug:
            qs = qs.filter(project__slug=project_slug, project__owner=self.request.user)
        external_id = self.request.query_params.get("external_id")
        if external_id:
            qs = qs.filter(external_id=external_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get", "post"])
    def entries(self, request, pk=None):
        session = self.get_object()

        if request.method.lower() == "get":
            qs = session.entries.all()
            tag = request.query_params.get("tag")
            if tag:
                qs = qs.filter(tag=tag)
            ser = MemoryEntrySerializer(qs, many=True)
            return Response(ser.data)

        serializer = MemoryEntrySerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        entry = MemoryEntry.objects.create(
            session=session,
            tag=serializer.validated_data.get("tag"),
            title=serializer.validated_data.get("title", ""),
            content=serializer.validated_data.get("content"),
            metadata=serializer.validated_data.get("metadata", {}),
        )
        return Response(MemoryEntrySerializer(entry).data, status=status.HTTP_201_CREATED)


class MemoryEntryViewSet(viewsets.ModelViewSet):
    """
    Memory entries, scoped to the authenticated user via session ownership.
    """
    serializer_class = MemoryEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [ApiTokenAuthentication]

    def get_queryset(self):
        qs = (
            MemoryEntry.objects.filter(session__user=self.request.user)
            .select_related("session", "session__project")
        )
        session_id = self.request.query_params.get("session")
        if session_id:
            qs = qs.filter(session_id=session_id)
        tag = self.request.query_params.get("tag")
        if tag:
            qs = qs.filter(tag=tag)
        project_slug = self.request.query_params.get("project")
        if project_slug:
            qs = qs.filter(session__project__slug=project_slug, session__project__owner=self.request.user)
        return qs

    def perform_create(self, serializer):
        # Require session_id and ensure ownership
        session_id = serializer.validated_data.get("session_id")
        if not session_id:
            raise ValidationError({"session_id": "This field is required."})
        try:
            session = Session.objects.get(id=session_id, user=self.request.user)
        except Session.DoesNotExist:
            raise NotFound("Session not found.")
        serializer.save(session=session)

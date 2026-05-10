"""API URL configuration using DRF routers."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, APITokenViewSet, AssetViewSet, SessionViewSet, MemoryEntryViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"tokens", APITokenViewSet, basename="token")
router.register(r"assets", AssetViewSet, basename="asset")
router.register(r"sessions", SessionViewSet, basename="session")
router.register(r"memory-entries", MemoryEntryViewSet, basename="memory-entry")

urlpatterns = [
    path("", include(router.urls)),
]

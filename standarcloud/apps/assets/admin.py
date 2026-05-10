"""Admin configuration for the assets app."""
from django.contrib import admin
from django.utils.html import format_html
from .models import Asset, SkillAsset, PromptAsset, AgentAsset, SpecAsset, OtherAsset

TYPE_COLORS = {
    Asset.TYPE_SKILL:  "#1565c0",
    Asset.TYPE_AGENT:  "#00897b",
    Asset.TYPE_PROMPT: "#6a1b9a",
    Asset.TYPE_SPEC:   "#e65100",
    Asset.TYPE_OTHER:  "#37474f",
}

# ---------------------------------------------------------------------------
# Shared base admin — reused by all proxy model admins
# ---------------------------------------------------------------------------

class AssetBaseAdmin(admin.ModelAdmin):
    list_display = (
        "name", "project", "type_badge", "path",
        "size_bytes", "content_hash_short", "updated_at",
    )
    list_filter = ("project", "updated_at")
    search_fields = ("name", "path", "project__name", "content_hash")
    readonly_fields = ("id", "asset_type", "content_hash", "size_bytes", "created_at", "updated_at")
    ordering = ("project", "name")
    fieldsets = (
        (None, {
            "fields": ("id", "project", "name", "asset_type", "path"),
        }),
        ("Content", {
            "fields": ("content",),
        }),
        ("Metadata", {
            "fields": ("content_hash", "size_bytes", "created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Type")
    def type_badge(self, obj):
        color = TYPE_COLORS.get(obj.asset_type, "#37474f")
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;'
            'border-radius:4px;font-size:11px;">{}</span>',
            color, obj.get_asset_type_display()
        )

    @admin.display(description="Hash")
    def content_hash_short(self, obj):
        return obj.content_hash[:12] + "…" if obj.content_hash else "—"


# ---------------------------------------------------------------------------
# Full Asset admin (all types visible together)
# ---------------------------------------------------------------------------

@admin.register(Asset)
class AssetAdmin(AssetBaseAdmin):
    list_display = (
        "name", "project", "type_badge", "path",
        "size_bytes", "content_hash_short", "updated_at",
    )
    list_filter = ("asset_type", "project", "updated_at")
    # asset_type is editable here so the user can change the type
    readonly_fields = ("id", "content_hash", "size_bytes", "created_at", "updated_at")


# ---------------------------------------------------------------------------
# Proxy model admins — one section per asset type
# ---------------------------------------------------------------------------

@admin.register(SkillAsset)
class SkillAssetAdmin(AssetBaseAdmin):
    """Admin for Skill assets only."""

    def get_queryset(self, request):
        return super().get_queryset(request).filter(asset_type=Asset.TYPE_SKILL)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        # Hide asset_type — it is fixed for this proxy
        return [f for f in fields if f != "asset_type"]


@admin.register(PromptAsset)
class PromptAssetAdmin(AssetBaseAdmin):
    """Admin for Prompt assets only."""

    def get_queryset(self, request):
        return super().get_queryset(request).filter(asset_type=Asset.TYPE_PROMPT)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        return [f for f in fields if f != "asset_type"]


@admin.register(AgentAsset)
class AgentAssetAdmin(AssetBaseAdmin):
    """Admin for Agent assets only."""

    def get_queryset(self, request):
        return super().get_queryset(request).filter(asset_type=Asset.TYPE_AGENT)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        return [f for f in fields if f != "asset_type"]


@admin.register(SpecAsset)
class SpecAssetAdmin(AssetBaseAdmin):
    """Admin for Spec assets only."""

    def get_queryset(self, request):
        return super().get_queryset(request).filter(asset_type=Asset.TYPE_SPEC)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        return [f for f in fields if f != "asset_type"]


@admin.register(OtherAsset)
class OtherAssetAdmin(AssetBaseAdmin):
    """Admin for Other assets."""

    def get_queryset(self, request):
        return super().get_queryset(request).filter(asset_type=Asset.TYPE_OTHER)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        return [f for f in fields if f != "asset_type"]

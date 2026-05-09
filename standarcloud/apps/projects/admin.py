"""Admin configuration for the projects app."""
from django.contrib import admin
from django.utils.html import format_html
from .models import Project, ProjectConfig


class ProjectConfigInline(admin.StackedInline):
    model = ProjectConfig
    can_delete = False
    verbose_name = "Configuration"
    verbose_name_plural = "Configuration"
    fields = ("visibility", "auto_backup", "backup_schedule", "extra")
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "owner", "visibility_badge", "asset_count", "created_at", "updated_at")
    list_filter = ("created_at", "config__visibility")
    search_fields = ("name", "slug", "description", "owner__username", "owner__email")
    readonly_fields = ("id", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-created_at",)
    inlines = [ProjectConfigInline]
    fieldsets = (
        (None, {
            "fields": ("id", "owner", "name", "slug", "description"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Visibility")
    def visibility_badge(self, obj):
        try:
            vis = obj.config.visibility
        except AttributeError:
            return format_html('<span style="color:#999;">—</span>')
        color = "#2e7d32" if vis == "public" else "#b71c1c"
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;'
            'border-radius:4px;font-size:11px;">{}</span>',
            color, vis.upper()
        )

    @admin.display(description="Assets")
    def asset_count(self, obj):
        count = obj.assets.count()
        return count if count else "—"


@admin.register(ProjectConfig)
class ProjectConfigAdmin(admin.ModelAdmin):
    list_display = ("project", "visibility", "auto_backup", "backup_schedule")
    list_filter = ("visibility", "auto_backup")
    search_fields = ("project__name", "project__slug")
    readonly_fields = ("project",)

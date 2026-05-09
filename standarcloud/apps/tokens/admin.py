"""Admin configuration for the tokens app."""
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import ApiToken


@admin.register(ApiToken)
class ApiTokenAdmin(admin.ModelAdmin):
    list_display = (
        "name", "user", "token_masked", "is_active",
        "status_badge", "created_at", "last_used_at", "expires_at",
    )
    list_filter = ("is_active", "created_at", "expires_at")
    search_fields = ("name", "user__username", "user__email")
    readonly_fields = ("id", "token", "created_at", "last_used_at")
    ordering = ("-created_at",)
    fieldsets = (
        (None, {
            "fields": ("id", "user", "name", "is_active"),
        }),
        ("Token", {
            "fields": ("token",),
            "description": "The token value is shown only once at creation.",
        }),
        ("Expiry & Usage", {
            "fields": ("expires_at", "last_used_at", "created_at"),
        }),
    )

    @admin.display(description="Token")
    def token_masked(self, obj):
        return obj.mask()

    @admin.display(description="Status", boolean=False)
    def status_badge(self, obj):
        now = timezone.now()
        if not obj.is_active:
            color, label = "#b71c1c", "Inactive"
        elif obj.expires_at and obj.expires_at < now:
            color, label = "#e65100", "Expired"
        else:
            color, label = "#2e7d32", "Active"
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;'
            'border-radius:4px;font-size:11px;">{}</span>',
            color, label
        )

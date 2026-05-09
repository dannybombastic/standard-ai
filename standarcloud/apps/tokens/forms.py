"""Forms for tokens app."""
from django import forms
from .models import ApiToken


class ApiTokenCreateForm(forms.ModelForm):
    """Token create form with a proper datetime widget for expires_at."""

    expires_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
        help_text="Optional. Local datetime (will be stored as timezone-aware if USE_TZ=True).",
    )

    class Meta:
        model = ApiToken
        fields = ["name", "expires_at"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }

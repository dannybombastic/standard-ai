"""Forms for assets app."""
from django import forms
from .models import Asset


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["asset_type", "name", "path", "content"]
        widgets = {
            "asset_type": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "path": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. skills/my-skill.md"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 16}),
        }
        help_texts = {
            "path": "Relative path within the project (unique per project).",
        }


class AssetQuickCreateForm(AssetForm):
    """Form variant used for 'Create Skill/Prompt/Spec' flows.

    Hides asset_type in the UI and forces it server-side.
    """

    def __init__(self, *args, forced_type: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.forced_type = forced_type
        if forced_type:
            self.fields["asset_type"].initial = forced_type
            self.fields["asset_type"].disabled = True

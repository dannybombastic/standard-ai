"""Forms for assets app."""
from django import forms
from django.utils.text import slugify

from .models import Asset


ENVIRONMENT_CHOICES = [
    (".github", ".github"),
    (".opencode", ".opencode"),
    (".claude", ".claude"),
]

PATH_CONTEXT_CHOICES = [
    ("skills", "skills"),
    ("prompts", "prompts"),
    ("agents", "agents"),
    ("specs", "specs"),
    ("assets", "assets"),
]


def _default_context_for_type(asset_type: str) -> str:
    if asset_type == Asset.TYPE_SKILL:
        return "skills"
    if asset_type == Asset.TYPE_AGENT:
        return "agents"
    if asset_type == Asset.TYPE_PROMPT:
        return "prompts"
    if asset_type == Asset.TYPE_SPEC:
        return "specs"
    return "assets"


def _suffix_for_context(path_context: str) -> str:
    if path_context == "agents":
        return ".agent.md"
    if path_context == "skills":
        return ".skill.md"
    if path_context == "prompts":
        return ".prompt.md"
    if path_context == "specs":
        return ".spec.md"
    return ".md"


def _compose_asset_path(environment_root: str, path_context: str, name: str) -> str:
    base_name = slugify(name) or "asset"
    suffix = _suffix_for_context(path_context)
    return f"{environment_root}/{path_context}/{base_name}{suffix}"


def _parse_path_defaults(path: str) -> tuple[str, str]:
    default_env = ".github"
    default_context = "assets"
    if not path:
        return default_env, default_context

    for root in (".github", ".opencode", ".claude"):
        prefix = f"{root}/"
        if path.startswith(prefix):
            tail = path[len(prefix):]
            for context in ("agents", "prompts", "skills", "specs", "assets"):
                if tail.startswith(f"{context}/"):
                    return root, context
            return root, default_context
    return default_env, default_context


class AssetForm(forms.ModelForm):
    environment_root = forms.ChoiceField(
        choices=ENVIRONMENT_CHOICES,
        label="Environment",
        initial=".github",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    path_context = forms.ChoiceField(
        choices=PATH_CONTEXT_CHOICES,
        label="Context",
        initial="assets",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Asset
        fields = ["asset_type", "name", "environment_root", "path_context", "path", "content"]
        widgets = {
            "asset_type": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "path": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 16}),
        }
        help_texts = {
            "path": "Generated from Environment + Context + Name.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_type = self.initial.get("asset_type") or getattr(self.instance, "asset_type", Asset.TYPE_OTHER)
        self.fields["path_context"].initial = _default_context_for_type(current_type)

        instance_path = getattr(self.instance, "path", "") if getattr(self.instance, "pk", None) else ""
        env_default, context_default = _parse_path_defaults(instance_path)
        if instance_path:
            self.fields["environment_root"].initial = env_default
            self.fields["path_context"].initial = context_default

        initial_name = self.initial.get("name") or getattr(self.instance, "name", "")
        if initial_name:
            self.initial["path"] = _compose_asset_path(
                str(self.fields["environment_root"].initial),
                str(self.fields["path_context"].initial),
                str(initial_name),
            )

    def clean(self):
        cleaned = super().clean()
        asset_type = str(cleaned.get("asset_type") or Asset.TYPE_OTHER)
        name = str(cleaned.get("name") or "")
        environment_root = str(cleaned.get("environment_root") or ".github")
        path_context = str(cleaned.get("path_context") or _default_context_for_type(asset_type))

        if path_context == "agents" and asset_type != Asset.TYPE_AGENT:
            raise forms.ValidationError("Agents context requires asset type 'Agent'.")

        composed_path = _compose_asset_path(environment_root, path_context, name)
        cleaned["path"] = composed_path
        self.instance.path = composed_path
        return cleaned


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
            self.fields["path_context"].initial = _default_context_for_type(forced_type)

    def clean(self):
        cleaned = super().clean()
        if self.forced_type:
            cleaned["asset_type"] = self.forced_type
            self.instance.asset_type = self.forced_type
        return cleaned

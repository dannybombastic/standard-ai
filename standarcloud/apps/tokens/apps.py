"""Tokens app config."""
from django.apps import AppConfig


class TokensConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "standarcloud.apps.tokens"
    label = "tokens"

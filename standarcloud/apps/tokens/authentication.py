"""DRF custom authentication using ApiToken."""
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import ApiToken


class ApiTokenAuthentication(BaseAuthentication):
    """Authenticate via 'Authorization: Token <token>' header."""

    keyword = "Token"

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith(f"{self.keyword} "):
            return None

        raw_token = auth_header[len(self.keyword) + 1:].strip()
        return self._authenticate_token(raw_token)

    def _authenticate_token(self, raw_token: str):
        try:
            api_token = ApiToken.objects.select_related("user").get(
                token=raw_token, is_active=True
            )
        except ApiToken.DoesNotExist:
            raise AuthenticationFailed("Invalid or inactive token.")

        if api_token.expires_at and api_token.expires_at < timezone.now():
            raise AuthenticationFailed("Token has expired.")

        # Update last_used_at without triggering full save
        ApiToken.objects.filter(pk=api_token.pk).update(last_used_at=timezone.now())

        return (api_token.user, api_token)

    def authenticate_header(self, request):
        return self.keyword

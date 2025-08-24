from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

class CookieJWTAuthentication(JWTAuthentication):
    """
    Extends JWTAuthentication to also check for JWT tokens in cookies.
    """
    def authenticate(self, request):
        # Try standard header authentication first
        header_auth = super().authenticate(request)
        if header_auth is not None:
            return header_auth

        # Fallback to cookies
        access_cookie_name = getattr(settings, 'JWT_ACCESS_COOKIE_NAME', 'access')
        raw_token = request.COOKIES.get(access_cookie_name)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

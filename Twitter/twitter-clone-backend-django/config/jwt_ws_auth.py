from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token = self._extract_token(scope)
        scope["user"] = await self._get_user(token)
        return await super().__call__(scope, receive, send)

    def _extract_token(self, scope):
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        query_token = (query_params.get("token") or [None])[0]
        if query_token:
            return query_token

        headers = dict(scope.get("headers", []))
        cookie_header = headers.get(b"cookie", b"").decode()
        cookies = {}
        if cookie_header:
            parts = cookie_header.split(";")
            for part in parts:
                if "=" in part:
                    key, value = part.strip().split("=", 1)
                    cookies[key] = value
        return cookies.get("accessToken")

    @database_sync_to_async
    def _get_user(self, token):
        from django.contrib.auth.models import AnonymousUser
        from rest_framework_simplejwt.authentication import JWTAuthentication
        from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

        if not token:
            return AnonymousUser()

        auth = JWTAuthentication()
        try:
            validated_token = auth.get_validated_token(token)
            return auth.get_user(validated_token)
        except (InvalidToken, TokenError):
            return AnonymousUser()


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)

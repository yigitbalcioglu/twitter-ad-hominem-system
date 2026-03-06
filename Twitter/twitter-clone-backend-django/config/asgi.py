import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

from config.jwt_ws_auth import JWTAuthMiddlewareStack
from config.routing import websocket_router

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
	{
		"http": django_asgi_app,
		"websocket": JWTAuthMiddlewareStack(websocket_router),
	}
)

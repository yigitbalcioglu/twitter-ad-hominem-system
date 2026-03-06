from channels.routing import URLRouter

from apps.users.routing import websocket_urlpatterns

websocket_router = URLRouter(websocket_urlpatterns)

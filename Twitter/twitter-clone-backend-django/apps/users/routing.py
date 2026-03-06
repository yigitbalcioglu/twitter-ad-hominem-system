from django.urls import re_path

from apps.users.consumers import DirectMessageConsumer

websocket_urlpatterns = [
    re_path(r"^ws/messages/(?P<user_id>[0-9a-f-]{36})/$", DirectMessageConsumer.as_asgi()),
]

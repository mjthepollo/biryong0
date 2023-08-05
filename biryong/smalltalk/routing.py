# chat/routing.py
from django.urls import re_path

from biryong.smalltalk import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/twitch_chat/(?P<room_name>\w+)/$", consumers.TwitchChatConsumer.as_asgi()),
    re_path(r"ws/smalltalk/(?P<room_name>\w+)/$", consumers.SmallTalkConsumer.as_asgi()),
]

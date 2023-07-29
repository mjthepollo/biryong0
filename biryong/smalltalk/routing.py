# chat/routing.py
from django.urls import re_path

from biryong.smalltalk import consumers

websocket_urlpatterns = [
    re_path(r"ws/smalltalk/(?P<room_name>\w+)/$", consumers.SmallTalkConsumer.as_asgi()),
]

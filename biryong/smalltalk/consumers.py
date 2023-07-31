import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils.html import escape

from biryong.smalltalk.models import SmallTalk


def get_talk(user, message):
    return {"user_id": user.username, "nickname": user.nickname,
            "thumbnail_image_url": user.thumbnail_image_url, "message": message, }


class SmallTalkConsumer(WebsocketConsumer):
    connected_users = set()

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # Join room group
        self.connected_users.add(self.scope["user"])
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "send_user_list"}
        )
        self.send_previous_messages({"start_index": 0, "end_index": None})

    def disconnect(self, close_code):
        # Leave room group
        self.connected_users.remove(self.scope["user"])
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "send_user_list"}
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = self.scope["user"]
        data_type = text_data_json["type"]
        if data_type == "message":
            message = escape(text_data_json["content"])
            SmallTalk.objects.create(user=user, message=message)
            talk = get_talk(user, message)
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "talk": talk}
            )
        else:
            raise Exception("Unknown data type.")

    def send_previous_messages(self, event):
        start_index = event.get("start_index", 0)
        end_index = event.get('end_index', None)
        created_time = datetime.datetime.now() - datetime.timedelta(minutes=60)
        recent_talks = SmallTalk.objects.filter(created__gte=created_time)
        previous_talks = recent_talks[start_index:end_index] if end_index\
            else recent_talks[start_index:]
        previous_talks = [get_talk(talk.user, talk.message) for talk in previous_talks]
        self.send(text_data=json.dumps({"type": "previous_talks", "previous_talks": previous_talks}))

    def send_user_list(self, event):
        user_list_info = []
        for user in self.connected_users:
            user_info = {"nickname": user.nickname,
                         "thumbnail_image_url": user.thumbnail_image_url,
                         }
            user_list_info.append(user_info)
        print(user_list_info)
        self.send(text_data=json.dumps({"type": "user_info_list", "user_info_list": user_list_info}))

    # Receive message from room group
    def chat_message(self, event):
        talk = event["talk"]
        # Send message to WebSocket
        print(talk)
        self.send(text_data=json.dumps({"type": "talk", "talk": talk}))

import json
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .utils import printPDF, update, refresh_db
import time
from django.contrib.auth.models import AnonymousUser


class WSConsumer(JsonWebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("WS", self.channel_name)
        self.accept()
        self.user = self.scope["user"]
        if isinstance(self.user, AnonymousUser):
            self.close()

    def receive_json(self, content, **kwargs):
        if content["type"] == "refresh":
            #time.sleep(5)
            refresh_db()
            self.send_json(content={"type":"DB_Refresh"})
        # elif content["type"] == "print":
        #     printPDF()
        elif content["type"] == "update":
            update(content["id"])

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "WS", self.channel_name)

    def WS_Send(self, event):
        self.send_json(content=event["data"])

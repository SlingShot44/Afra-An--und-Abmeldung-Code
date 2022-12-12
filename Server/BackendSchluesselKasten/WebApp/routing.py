from django.urls import path
from .consumers import WSConsumer

websocket_urlpatterns = [
    path("ws/", WSConsumer.as_asgi()),
]

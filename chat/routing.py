from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('chat/', consumers.ChatConsumer.as_asgi()),
    path('chat/<int:vendor_id>', consumers.ChatConsumer.as_asgi()),
]
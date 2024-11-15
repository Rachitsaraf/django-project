from django.urls import re_path
from . import consumers  # Adjust based on your project's structure

# Define WebSocket URL patterns for different functionalities
websocket_urlpatterns = [
    # WebSocket connection for text chat and file sharing
    re_path(r'ws/chat/(?P<room_slug>[\w\s%]+)/$', consumers.ChatConsumer.as_asgi()),

    # WebSocket connection for video calling
    re_path(r'ws/video/(?P<room_slug>[\w\s%]+)/$', consumers.ChatConsumer.as_asgi()),

    # Add more routes as necessary for other functionalities (e.g., bot interactions, etc.)
]

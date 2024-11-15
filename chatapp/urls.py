from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'chatapp'  # Ensure this is defined

urlpatterns = [
    # URL for the rooms view
    path("", views.rooms, name="rooms"),

    # Dynamic URL for individual room view based on slug
    path('chat/<slug:slug>/', views.room, name='chat_room'),

    # URL for chatbot message functionality
    path("chatbot/", views.chatbot_response, name="chatbot_message"),

    # Video signal endpoint for WebRTC signaling
    path('video-signal/', views.video_signal, name='video_signal'),  # Added for video call functionality
]

# Serve media files during development (only works if DEBUG=True in settings)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

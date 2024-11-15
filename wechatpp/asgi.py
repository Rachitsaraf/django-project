import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from wechatpp.routing import websocket_urlpatterns  # Correct import for websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wechatpp.settings')

# Initialize Django ASGI application
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Only pass websocket_urlpatterns here
        )
    ),
})

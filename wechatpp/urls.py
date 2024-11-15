"""
URL configuration for wechatpp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from chatapp import views  # Import views from the chatapp app

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # Authentication URLs (login, logout, password management)
    path("accounts/", include("django.contrib.auth.urls")),

    # Custom signup URL for new user registration
    path('signup/', views.signup, name='signup'),

    # Main app URLs: Includes all routes from chatapp.urls with namespace 'chatapp'
    path('chatapp/', include(('chatapp.urls', 'chatapp'), namespace='chatapp')),

    # Home page URL: Redirects to chatapp's rooms view or homepage
    path('', views.rooms, name='home'),  # Sets 'rooms' as the home page view

    # Chat room URL for individual rooms
    path('<slug:slug>/', views.room, name='chat_room'),  # URL for a specific chat room
]

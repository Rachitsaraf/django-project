# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Room Model
class Room(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=100, unique=True)  # Ensure slug is unique for each room

    def __str__(self):
        return f"Room: {self.name} | ID: {self.slug}"


# Message Model
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")  # Linking message to room
    created_on = models.DateTimeField(auto_now_add=True)  # Created timestamp
    file = models.FileField(upload_to='uploads/', null=True, blank=True)  # Optional file upload

    def __str__(self):
        return f"Message by {self.user.username} in {self.room.name} at {self.formatted_time()}"

    def formatted_time(self):
        """Return formatted message creation time"""
        return timezone.localtime(self.created_on).strftime('%H:%M:%S')


# UserStatus Model to track online/offline status
class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="status")
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {'Online' if self.is_online else 'Offline'} (Last seen: {self.last_seen})"

    def set_online(self):
        """Mark the user as online and update last seen"""
        self.is_online = True
        self.last_seen = timezone.now()
        self.save()

    def set_offline(self):
        """Mark the user as offline and update last seen"""
        self.is_online = False
        self.last_seen = timezone.now()
        self.save()

    def update_last_seen(self):
        """Update the last seen timestamp"""
        self.last_seen = timezone.now()
        self.save()

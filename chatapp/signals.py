from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserStatus

@receiver(post_save, sender=User)
def update_user_status(sender, instance, created, **kwargs):
    if created:
        # Create a new UserStatus instance if the User was just created
        UserStatus.objects.create(user=instance, is_online=True)
    else:
        # If UserStatus already exists, update the is_online status
        if hasattr(instance, 'status'):
            user_status = instance.status
            user_status.is_online = True
            user_status.save()
        else:
            # Create UserStatus if it doesn't exist (in case of any issues)
            UserStatus.objects.create(user=instance, is_online=True)

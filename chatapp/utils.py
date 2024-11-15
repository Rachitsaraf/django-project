from django.utils import timezone

def format_time(timestamp):
    return timezone.localtime(timestamp).strftime('%H:%M:%S')

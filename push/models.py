from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import signals
from webpush import send_user_notification
from webpush.utils import send_to_subscription

class TestUsed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=200)

    def __str__(self):
        return self.name

@receiver(signals.post_save, sender=TestUsed)
def save_me(sender, instance, created, **kwargs):
    if kwargs.get('created', True):
        payload = {"head": "Welcome", "body": "This is my testing"}
        user = instance.user
        send_user_notification(user=user, payload=payload, ttl=1000)
# Create your models here.


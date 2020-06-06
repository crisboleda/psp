
# Django
from django.db import models

# Models
from django.contrib.auth.models import User


# This model save the notifications of the user
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications')
    message = models.CharField(max_length=60, help_text='message of notification')
    was_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
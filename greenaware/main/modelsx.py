from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user_id = models.CharField(max_length=50, unique=True)
    user_role = models.CharField(max_length=20, default='user')
    api_key = models.CharField(max_length=100, blank=True, null=True)
    subscription_package = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.user.username
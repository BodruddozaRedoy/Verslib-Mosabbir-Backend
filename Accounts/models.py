from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default="avatar.svg")
    premium = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.email and not self.username:  # auto-generate username
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)
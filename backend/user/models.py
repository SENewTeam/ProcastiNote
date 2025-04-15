from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    profile = models.CharField(max_length=10,default="scholar")
    created_at = models.DateTimeField(default=timezone.now)
    papers = models.CharField(max_length=1000,default="")
    papersAccessTime = models.JSONField(default=dict)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


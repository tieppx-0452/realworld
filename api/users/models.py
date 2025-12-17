from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        ordering = ['-id']

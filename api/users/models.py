from core.models import CoreModel
from django.db import models
from django.contrib.auth.models import AbstractUser

import core.constants as constants

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        ordering = ['-id']

class Following(CoreModel):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )

    class Meta:
        db_table = 'followings'
        unique_together = ('follower_id', 'following_id')
        ordering = ['-createdAt']

from django.db import models
from core.models import CoreModel

import core.constants as constants

class Article(CoreModel):
    title = models.CharField(max_length=constants.MAX_LENGTH, null=False)
    slug = models.SlugField(unique=True, max_length=constants.MAX_LENGTH, null=True)
    description = models.TextField(null=False)
    body = models.TextField(null=False)
    isPublished = models.BooleanField(default=False)
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='articles'
    )

    class Meta:
        db_table = 'articles'
        ordering = ['-id']

class Comment(CoreModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = models.TextField(null=False)

    class Meta:
        db_table = 'comments'
        ordering = ['-id']

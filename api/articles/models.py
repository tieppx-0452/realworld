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
    favorited_by = models.ManyToManyField(
        'users.User',
        through='FavoriteArticle',
        related_name='favorites'
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

class Tag(CoreModel):
    name = models.CharField(max_length=constants.MAX_LENGTH, unique=True, null=False)

    class Meta:
        db_table = 'tags'
        ordering = ['-id']

class ArticleTag(CoreModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='article_tags'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='article_tags'
    )

    class Meta:
        db_table = 'article_tags'
        unique_together = ('article_id', 'tag_id')
        ordering = ['-id']

class FavoriteArticle(CoreModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='favorite_articles'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='favorite_articles'
    )

    class Meta:
        db_table = 'favorite_articles'
        unique_together = ('user_id', 'article_id')
        ordering = ['-createdAt']

from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255, null=False)
    slug = models.SlugField(unique=True, max_length=255, null=True)
    description = models.TextField(null=False)
    body = models.TextField(null=False)
    isPublished = models.BooleanField(default=False)
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='articles'
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'articles'
        ordering = ['-id']

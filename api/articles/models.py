from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='articles'
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)
    is_published = models.BooleanField(default=False)

    class Meta:
        db_table = 'articles'
        ordering = ['-id']

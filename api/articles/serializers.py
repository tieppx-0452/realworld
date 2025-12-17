from rest_framework import serializers
from .models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):
    comments = serializers
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'body',
            'isPublished',
            'author',
            'createdAt',
            'updatedAt',
        ]

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'article',
            'author',
            'body',
            'createdAt',
            'updatedAt',
        ]

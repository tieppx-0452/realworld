from rest_framework import serializers
from .models import Article, Comment
from rest_framework.serializers import (
    SerializerMethodField,
    CharField,
)

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

class CommentGetSerializer(serializers.ModelSerializer):
    author = SerializerMethodField()

    def get_author(self, obj):
        return {
            "username": obj.author.username,
            "email": obj.author.email,
            "bio": obj.author.bio,
            "image": obj.author.image,
        }

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

class CommentPostSerializer(serializers.Serializer):
    body = serializers.CharField(max_length=1000, required=True)

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

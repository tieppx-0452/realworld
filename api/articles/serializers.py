from rest_framework import serializers
from ..users.serializers import RelatedUserSerializer
from .models import Article, Comment
from rest_framework.serializers import (
    SerializerMethodField,
    CharField,
)
from django.utils.timezone import now

class ArticleSerializer(serializers.ModelSerializer):
    comments = SerializerMethodField()
    author = SerializerMethodField()
    favorited_by = SerializerMethodField()

    def get_favorited_by(self, obj):
        users = obj.favorited_by.all().order_by('-createdAt')
        return [RelatedUserSerializer(user).data for user in users]

    def get_author(self, obj):
        return RelatedUserSerializer(obj.author).data

    def get_comments(self, obj):
        return CommentGetSerializer(
            obj.comments.all().order_by('-createdAt'),
            many=True
        ).data

    def generate_slug(title):
        return f"{title.strip().lower().replace(' ', '-')}-{int(now().timestamp())}"

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
            'comments',
            'favorited_by',
            'createdAt',
            'updatedAt',
        ]

class CommentGetSerializer(serializers.ModelSerializer):
    author = SerializerMethodField()

    def get_author(self, obj):
        return RelatedUserSerializer(obj.author).data

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
    body = serializers.CharField(required=True)

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

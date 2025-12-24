from rest_framework import serializers
from ..users.serializers import RelatedUserSerializer
from .models import Article, Comment, Tag, ArticleTag
from rest_framework.serializers import (
    SerializerMethodField,
    CharField,
)
from django.utils.timezone import now

class ArticleSerializer(serializers.ModelSerializer):
    comments = SerializerMethodField()
    author = SerializerMethodField()
    favorited_by = SerializerMethodField()
    tags = SerializerMethodField()

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

    def get_tags(self, obj):
        article_tags = obj.article_tags.all().order_by('tag__name')
        return [article_tag.tag.name for article_tag in article_tags]

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
            'tags',
            'createdAt',
            'updatedAt',
        ]

class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    def generate_slug(title):
        return f"{title.strip().lower().replace(' ', '-')}-{int(now().timestamp())}"

    def save_article_tag(article, tag_names):
        if not tag_names:
            return
        tag_titles = [tag.strip() for tag in tag_names.split(',') if tag.strip()]
        for tag_title in tag_titles:
            tag, _ = Tag.objects.get_or_create(name=tag_title)
            ArticleTag.objects.get_or_create(article=article, tag=tag)

    class Meta:
        model = Article
        fields = [
            'title',
            'slug',
            'description',
            'body',
            'author',
            'isPublished',
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

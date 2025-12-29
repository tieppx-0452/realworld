from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from .models import Article, Comment, Tag, FavoriteArticle, ArticleTag
from .serializers import ArticleSerializer, ArticleCreateUpdateSerializer, CommentGetSerializer, CommentPostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from ..pagination import BasePagination
from .filtering import FilterArticle

class ArticleListCreate(generics.ListCreateAPIView):
    pagination_class = BasePagination
    filter_backends = [FilterArticle]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        queryset = Article.objects.all()
        queryset = self.filter_queryset(queryset)
        queryset = queryset.order_by('-id')
        page = self.paginate_queryset(queryset)
        serializer = ArticleSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id
        data['slug'] = ArticleCreateUpdateSerializer.generate_slug(data['title'])
        serializer = ArticleCreateUpdateSerializer(data=data)
        if serializer.is_valid():
            article = serializer.save()
            ArticleCreateUpdateSerializer.save_article_tag(article, data.get('tagList', ''))
            return Response(serializer.data)
        return Response(serializer.errors)

class ArticleRetrieve(generics.RetrieveAPIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        if article.author.id != request.user.id:
            return Response({
                "message": "You do not have permission to update this article."
            })
        data = request.data.copy()
        data['slug'] = ArticleSerializer.generate_slug(data['title'])
        serializer = ArticleSerializer(article, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            ArticleCreateUpdateSerializer.save_article_tag(article, data.get('tagList', ''))
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        if article.author.id != request.user.id:
            return Response({
                "message": "You do not have permission to delete this article."
            })
        article.delete()
        return Response({
            "message": "Article deleted successfully."
        })

class FeedArticleList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.values_list('following_id', flat=True)
        if not following_users:
            return Response({
                "articles": [],
                "articlesCount": 0
            })
        queryset = Article.objects.filter(author_id__in=following_users)
        queryset = queryset.order_by('-id')
        page = self.paginate_queryset(queryset)
        serializer = ArticleSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

class CommentListCreate(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        comments = article.comments.all().order_by("-id")
        serializer = CommentGetSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        data = request.data.copy()
        data['author'] = request.user
        data['article'] = article
        serializer = CommentPostSerializer(data=data)
        if serializer.is_valid():
            Comment.objects.create(
                article=article,
                author=request.user,
                body=serializer.validated_data['body']
            )
            return Response(serializer.data)
        return Response(serializer.errors)

class CommentRetrieve(generics.RetrieveAPIView):
    def delete(self, request, slug, id):
        article = get_object_or_404(Article, slug=slug)
        comment = article.comments.filter(id=id).first()
        if not comment:
            return Response({
                "message": "Comment not found."
            })
        if comment.author.id != request.user.id:
            return Response({
                "message": "You do not have permission to delete this comment."
            })
        comment.delete()
        return Response({
            "message": "Comment deleted successfully."
        })

class TagList(generics.ListAPIView):
    def get(self, request):
        tags = Tag.objects.all().order_by("-id")
        tag_names = [tag.name for tag in tags]
        return Response({
            "tags": tag_names
        })

class ArticleFavorite(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        favorite_exists = FavoriteArticle.objects.filter(
            user=request.user,
            article=article
        ).exists()
        if favorite_exists:
            return Response({
                "message": "Article already favorited."
            })
        FavoriteArticle.objects.create(
            user=request.user,
            article=article
        )
        return Response({
            "message": "Article favorited successfully."
        })

    def delete(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        favorite_exists = FavoriteArticle.objects.filter(
            user=request.user,
            article=article
        ).first()
        if not favorite_exists:
            return Response({
                "message": "Article is not favorited."
            })
        favorite_exists.delete()
        return Response({
            "message": "Article unfavorited successfully."
        })

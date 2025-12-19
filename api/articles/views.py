from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentGetSerializer, CommentPostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes

class ArticleListCreate(generics.ListCreateAPIView):
    def get(self, request):
        queryset = Article.objects.all().order_by("-id")
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id
        data['slug'] = ArticleSerializer.generate_slug(data['title'])
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class ArticleRetrieve(generics.RetrieveAPIView):
    def get(self, request, slug):
        article = Article.objects.filter(slug=slug).first()
        if not article:
            return Response({
                "message": "Article not found."
            })
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def put(self, request, slug):
        article = Article.objects.filter(slug=slug).first()
        if not article:
            return Response({
                "message": "Article not found."
            })
        if article.author.id != request.user.id:
            return Response({
                "message": "You do not have permission to delete this article."
            })
        data = request.data.copy()
        data['slug'] = ArticleSerializer.generate_slug(data['title'])
        serializer = ArticleSerializer(article, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @permission_classes([IsAuthenticated])
    def delete(self, request, slug):
        article = Article.objects.filter(slug=slug).first()
        if not article:
            return Response({
                "message": "Article not found."
            })
        if article.author.id != request.user.id:
            return Response({
                "message": "You do not have permission to delete this article."
            })
        article.delete()
        return Response({
            "message": "Article deleted successfully."
        })

class CommentListCreate(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, slug):
        article = Article.objects.filter(slug=slug).first()
        if not article:
            return Response({
                "message": "Article not found."
            })
        comments = article.comments.all().order_by("-id")
        serializer = CommentGetSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, slug):
        article = Article.objects.filter(slug=slug).first()
        if not article:
            return Response({
                "message": "Article not found."
            })
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

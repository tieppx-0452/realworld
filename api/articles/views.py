from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.utils.timezone import now

class ArticleListCreate(generics.ListCreateAPIView):
    def get(self, request):
        queryset = Article.objects.all().order_by("-id")
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id
        data['slug'] = f"{request.data['title'].strip().lower().replace(' ', '-')}-{int(now().timestamp())}"
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
        data['slug'] = f"{request.data['title'].strip().lower().replace(' ', '-')}-{int(now().timestamp())}"
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

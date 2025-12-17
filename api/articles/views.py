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

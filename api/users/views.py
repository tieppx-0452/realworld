from django.shortcuts import render
from rest_framework import generics
from .models import User
from .serializers import UserSerializer, AuthenticationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

class Authentication(generics.CreateAPIView):
    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        ).first()
        if not user:
            return Response({})
        token, created = Token.objects.get_or_create(user=user)
        data = UserSerializer(user).data
        data["token"] = token.key
        return Response(data)

class Registration(generics.CreateAPIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

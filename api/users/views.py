from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
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
            return Response({
                "message": "Wrong credentials."
            })
        token, created = Token.objects.get_or_create(user=user)
        data = UserSerializer(user).data
        data['token'] = token.key
        return Response(data)

class Registration(generics.CreateAPIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class AuthUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class Profile(generics.RetrieveAPIView):
    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({
                "message": "User not found."
            })
        serializer = UserSerializer(user)
        return Response(serializer.data)

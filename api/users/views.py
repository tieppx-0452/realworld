from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User, Following
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
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class FollowingUser(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        following_user = get_object_or_404(User, username=username)
        if following_user.id == request.user.id:
            return Response({
                "message": "You cannot follow yourself."
            })
        check_following_exists = Following.objects.filter(
            follower_id=request.user.id,
            following_id=following_user.id
        ).exists()
        if check_following_exists:
            return Response({
                "message": f"You are already following {username}."
            })
        Following.objects.create(
            follower_id=request.user.id,
            following_id=following_user.id
        )
        return Response({
            "message": f"You are now following {username}."
        })

    def delete(self, request, username):
        unfollow_user = get_object_or_404(User, username=username)
        check_following_exists = Following.objects.filter(
            follower_id=request.user.id,
            following_id=unfollow_user.id
        ).exists()
        if not check_following_exists:
            return Response({
                "message": f"You are not following {username}."
            })
        check_following_exists.delete()
        return Response({
            "message": f"You have unfollowed {username}."
        })

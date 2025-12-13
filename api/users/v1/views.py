from .models import User
from .serializers import UserSerializer
from rest_framework import generics, status
from realworld.views import BaseResponse

class UserList(generics.ListCreateAPIView):
    def get(self, request):
        queryset = User.objects.all().order_by("-id")
        serializer = UserSerializer(queryset, many=True)
        response = BaseResponse(
            serializer.data,
            code=status.HTTP_200_OK
        )
        return response.get_response()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = BaseResponse(
                serializer.data,
                code=status.HTTP_200_OK,
                messages=["User created successfully."]
            )
            return response.get_response()
        response = BaseResponse(
            {},
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            messages=serializer.errors
        )
        return response.get_response()

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        if not user:
            response = BaseResponse(
                {},
                code=status.HTTP_404_NOT_FOUND,
                messages=["User not found."]
            )
            return response.get_response()
        serializer = UserSerializer(user)
        response = BaseResponse(
            serializer.data,
            code=status.HTTP_200_OK
        )
        return response.get_response()

    def put(self, request, id):
        user = User.objects.filter(id=id).first()
        if not user:
            response = BaseResponse(
                {},
                code=status.HTTP_404_NOT_FOUND,
                messages=["User not found."]
            )
            return response.get_response()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = BaseResponse(
                serializer.data,
                code=status.HTTP_200_OK,
                messages=["User updated successfully."]
            )
            return response.get_response()
        response = BaseResponse(
            {},
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            messages=serializer.errors
        )
        return response.get_response()

    def delete(self, request, id):
        user = User.objects.filter(id=id)
        if not user:
            response = BaseResponse({}, code=status.HTTP_404_NOT_FOUND, messages=["User not found."])
            return response.get_response()
        user.delete()
        response = BaseResponse(
            {},
            code=status.HTTP_200_OK,
            messages=["User deleted successfully."]
        )
        return response.get_response()

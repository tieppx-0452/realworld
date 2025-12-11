from users.models import User
from users.serializers import UserSerializer
from rest_framework import generics
from realworld.views import BaseResponse

class UserList(generics.ListCreateAPIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        response = BaseResponse(serializer.data, code=200)
        return response.get_response()

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        response = BaseResponse(serializer.data, code=200)
        return response.get_response()

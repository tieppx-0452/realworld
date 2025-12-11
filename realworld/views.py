from rest_framework import generics
from rest_framework.response import Response

class BaseResponse:
    def __init__(self, data, code=200):
        self.validated_data = data
        self.code = code

    def get_response(self):
        return Response({
            "data": self.validated_data,
            "code": self.code
        })

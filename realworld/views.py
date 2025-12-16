from rest_framework import generics
from rest_framework.response import Response

class BaseResponse:
    def __init__(self, data, code=200, messages=None):
        self.validated_data = data
        self.code = code
        self.messages = messages if messages is not None else []

    def get_response(self):
        return Response({
            "data": self.validated_data,
            "code": self.code,
            "messages": self.messages
        })

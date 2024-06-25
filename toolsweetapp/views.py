from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

#Create views here

class TestAPIView(APIView):
    def get(self, request):
        data = {"message": "Hello from Django"}
        return Response(data)

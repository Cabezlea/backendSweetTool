from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q;
from .models import FLX_Log
from .serializers import FLXLogSerializer

#Create views here

class TestAPIView(APIView):
    def get(self, request, format=None):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        keyword = request.query_params.get('keyword', '')
        location = request.query_params.get('location', '')

        if not start_time or not end_time:
            return Response({"error": "Start time and end time are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetching data based on the parameters
        query = Q(Fecha__range=[start_time, end_time])

        if keyword:
            query &= Q(Mensaje__icontains=keyword)

        if location:
            query &= Q(Maquina__icontains=location)

        logs = FLX_Log.objects.filter(query)
        serializer = FLXLogSerializer(logs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q;
from .models import FLX_Log
from .serializers import FLXLogSerializer

#Create views here

class TestAPIView(APIView):
    def get(self, request):
        # Get search parameters from the request
        date = request.GET.get('date')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        receipt_number = request.GET.get('receipt_number')
        keyword = request.GET.get('keyword')
        location = request.GET.get('location')

        print(
            f"Received parameters: date={date}, start_time={start_time}, end_time={end_time}, receipt_number={receipt_number}, keyword={keyword}, location={location}")

        # Filter data based on the search parameters
        queryset = FLX_Log.objects.all()

        if date:
            queryset = queryset.filter(Fecha__date=date)
        if start_time and end_time:
            queryset = queryset.filter(Fecha__time__gte=start_time, Fecha__time__lte=end_time)
        if receipt_number:
            queryset = queryset.filter(Evento=receipt_number)
        if keyword:
            queryset = queryset.filter(Mensaje__icontains=keyword)
        if location:
            queryset = queryset.filter(Maquina=location)

        if not queryset.exists():
            return Response({"message": "No data found for the provided search criteria."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = FLXLogSerializer(queryset, many=True)
        return Response(serializer.data)

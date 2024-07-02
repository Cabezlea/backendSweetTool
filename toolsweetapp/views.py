from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import FLX_Log
from .serializers import FLXLogSerializer
import re

# Create views here

class TestAPIView(APIView):
    def get(self, request):
        # Get search parameters from the request
        date = request.GET.get('date')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        receipt_number = request.GET.get('receipt_number')
        keyword = request.GET.get('keyword')
        location = request.GET.get('location')
        terminal = request.GET.get('terminal')

        print(
            f"Received parameters: date={date}, start_time={start_time}, end_time={end_time}, receipt_number={receipt_number}, keyword={keyword}, location={location}, terminal={terminal}")

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
            # This assumes location is a part like 'PUNTILLA' from 'C1PUNTILLA-PC'
            queryset = queryset.filter(Maquina__regex=r'[A-Z]\d+' + location)

        if terminal:
            # Extract the terminal number and filter based on the number after the first uppercase letter
            terminal_number = re.findall(r'\d+', terminal)
            if terminal_number:
                terminal_number = terminal_number[0]
                queryset = queryset.filter(Maquina__regex=r'^[A-Z]' + terminal_number)
        if not queryset.exists():
            return Response({"message": "No data found for the provided search criteria."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = FLXLogSerializer(queryset, many=True)
        return Response(serializer.data)

class LocationAPIView(APIView):
    def get(self, request):
        # Extract unique locations from the Maquina field
        maquinas = FLX_Log.objects.values_list('Maquina', flat=True).distinct()
        locations = set()

        # Regex to extract location name after terminal number
        for maquina in maquinas:
            match = re.search(r'[A-Z]\d+([A-Z]+)', maquina)
            if match:
                locations.add(match.group(1))

        return Response(list(locations), status=status.HTTP_200_OK)

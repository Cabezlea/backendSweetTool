from rest_framework import serializers
from .models import FLX_Log

class FLXLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FLX_Log
        fields = ['Fecha', 'Evento', 'UsuarioAplicacion', 'Objeto', 'Mensaje', 'Maquina']
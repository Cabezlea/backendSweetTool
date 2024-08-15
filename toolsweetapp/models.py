from django.db import models

# Create your models here.

class FLX_Log(models.Model):
    Evento = models.BigAutoField(primary_key=True)
    Fecha = models.DateTimeField(auto_now_add=True)
    Maquina = models.CharField(max_length=255, default='')
    AplicacionFLX = models.CharField(max_length=128, blank=True, null=True)
    Aplicacion = models.CharField(max_length=128, default='')
    Empresa = models.IntegerField()
    Usuario = models.CharField(max_length=100, default='')
    UsuarioAplicacion = models.CharField(max_length=100, blank=True, null=True)
    Version = models.CharField(max_length=128, blank=True, null=True)
    Objeto = models.CharField(max_length=100)
    Mensaje = models.CharField(max_length=8000)

    class Meta:
        db_table = 'FLX_Log'

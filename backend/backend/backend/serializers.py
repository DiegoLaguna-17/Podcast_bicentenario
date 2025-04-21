# serializers.py

from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'usuario', 'contrasenia', 'correo', 'fecha_ingreso', 'rol']

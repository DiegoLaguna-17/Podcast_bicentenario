from django.db import models
from django.contrib.auth.hashers import make_password
import datetime

class Usuario(models.Model):
    idusuario = models.AutoField(primary_key=True, db_column='idusuario')  # Mapea a tu PK real
    usuario = models.CharField(max_length=100)
    contrasenia = models.CharField(max_length=128)
    correo = models.EmailField()
    fecha_ingreso = models.DateField(auto_now_add=True)
    rol = models.CharField(max_length=50)

    class Meta:
        db_table = 'backend_usuario'  # Nombre exacto de tu tabla en Supabase
        managed = False  # Evita que Django maneje las migraciones para esta tabla

    def __str__(self):
        return self.usuario


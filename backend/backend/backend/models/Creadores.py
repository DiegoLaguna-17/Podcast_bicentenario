
from django.db import models
from django.contrib.auth.hashers import make_password
class Creador(models.Model):
    idcreador=models.AutoField(primary_key=True,db_column='idcreador')
    usuario = models.CharField(max_length=100)
    contrasenia = models.CharField(max_length=128)
    nombre= models.CharField(max_length=128)
    correo = models.EmailField()
    fotoperfil=models.CharField(max_length=400)
    biografia=models.CharField(max_length=350)
    fecha_ingreso = models.DateField(auto_now_add=True)
    imgdonaciones= models.CharField(max_length=400)

    class Meta:
        db_table = 'backend_creadores'  # Nombre exacto de tu tabla en Supabase
        managed = False  # Evita que Django maneje las migraciones para esta tabla

    def __str__(self):
        return self.usuario


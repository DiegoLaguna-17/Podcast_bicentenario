# backend/utils/db_connection.py
import psycopg2
from psycopg2 import OperationalError
from django.conf import settings

def obtener_conexion():
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
            sslmode='require'
        )
        print("✅ ¡Conexión exitosa a Supabase!")  # Debug
        return conn
    except OperationalError as e:
        print(f"❌ Error de conexión: {e}")  # Debug detallado
        return None
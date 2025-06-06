# backend/views.py
from django.http import JsonResponse
from .db_connection import obtener_conexion
import json
# backend/views.py
from django.http import JsonResponse
import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import os
from .settings import SUPABASE_URL, SUPABASE_KEY,DEBUG
from supabase import create_client, Client
# views.py

from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
import os
import uuid  # Importar uuid para generar nombres únicos
from django.views.decorators.http import require_GET
# Configurar la conexión con Supabase
url = SUPABASE_URL
key = SUPABASE_KEY
supabase: Client = create_client(url, key)
# views.py
import logging
from django.utils import timezone 
logger = logging.getLogger(__name__)
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
import datetime
import jwt
from django.conf import settings
from django.http import JsonResponse
from .decorators import token_required
from django.http import JsonResponse
import random
import requests
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from django.http import JsonResponse
from django.utils import timezone
import traceback
import os
import uuid
##########################################################################################################################
@swagger_auto_schema(
    tags=['Login'],
    method='post',
    operation_description="Login de usuario enviando usuario, contraseña y rol",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['usuario', 'contrasenia', 'rol'],
        properties={
            'usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Correo o usuario'),
            'contrasenia': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña'),
            'rol': openapi.Schema(type=openapi.TYPE_STRING, description='Rol del usuario, ej: Creador, Administrador, Oyente'),
        }
    ),
    consumes=['application/json'],
    responses={
        200: openapi.Response(description="Código enviado correctamente"),
        400: 'Campos requeridos faltantes o error',
        401: 'Contraseña incorrecta',
        403: 'Rol no coincide o teléfono faltante',
        404: 'Usuario no encontrado',
        405: 'Método no permitido',
        500: 'Error interno'
    }
)
############################################################################
@api_view(['POST'])
@authentication_classes([])  # ❗ Desactiva autenticación
@permission_classes([AllowAny])
def login_usuario(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        usuario = request.data.get('usuario')
        contrasenia = request.data.get('contrasenia')
        rol = request.data.get('rol') 
        if not all([usuario, contrasenia, rol]):
            return JsonResponse({'error': 'Usuario, contraseña y rol son requeridos'}, status=400)
        if rol == 'Creador':
            user_id_field = 'idcreador'
            tabla = 'backend_creadores'
        elif rol in ['Administrador', 'Oyente']:
            tabla = 'backend_usuario'
            user_id_field = 'idusuario'
        else:
            return JsonResponse({'error': 'Rol no válido'}, status=400)
        response = supabase.table(tabla).select('*').eq('correo', usuario).execute()
        if not response.data:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        usuario_data = response.data[0]
        # Verificación de contraseña
        if not check_password( contrasenia,usuario_data.get('contrasenia')):
            return JsonResponse({'error': 'Contraseña incorrecta'}, status=401)
        # Verificar rol si está en la tabla
        if 'rol' in usuario_data and usuario_data['rol'] != rol:
            return JsonResponse({'error': 'El rol no coincide para este usuario'}, status=403)
        if not usuario_data['telefono']:
            return JsonResponse({'error': 'No hay telefono para este usuario'}, status=403)
        # Datos que irán dentro del token
        # Crear el payload con tiempo de expiración
        telefono=usuario_data['telefono']
        # Codificar el token con la clave secreta de Django
        respuest=enviar_codigo_whatsapp(telefono)
        codigo=respuest
        return JsonResponse({'mensaje':'Codigo enviado','validador':codigo,
                             'id':usuario_data[user_id_field],'rol':rol})
    except Exception as e:
        print("Error en login:", str(e))
        traceback.print_exc()  # 👈 esto imprimirá la traza completa del error
        return JsonResponse({'error': 'Error en el servidor'}, status=500)



def enviar_codigo_whatsapp(telefono):
    if not telefono:
        return JsonResponse({"error": "Número no proporcionado"}, status=400)

    codigo = str(random.randint(100000, 999999))
    print(f"Código generado: {codigo}")

    token = "0l5pdfxicmpxub44"
    url = "https://api.ultramsg.com/instance121270/messages/chat"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        "token": token,
        "to": telefono,
        "body": f"Tu código de inicio de sesión es: {codigo}",
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        # Puedes guardar también ID o rol si ya los tienes
        
        return codigo
    else:
        return JsonResponse({"error": "Error al enviar el mensaje", "detalles": response.json()}, status=500)
######################################################################################################################
@swagger_auto_schema(
    tags=['Login'],
    method='post',
    operation_description="Verifica el código enviado al usuario y genera un token JWT si es correcto.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['codigo', 'validador', 'id', 'rol'],
        properties={
            'codigo': openapi.Schema(type=openapi.TYPE_STRING, description='Código ingresado por el usuario'),
            'validador': openapi.Schema(type=openapi.TYPE_STRING, description='Código que fue enviado al usuario'),
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
            'rol': openapi.Schema(type=openapi.TYPE_STRING, description='Rol del usuario'),
        }
    ),
    responses={
        200: openapi.Response(description="Token generado correctamente"),
        401: 'Código incorrecto',
        405: 'Método no permitido'
    }
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def verificar_codigo(request):
    if request.method == "POST":
        codigo_ingresado = request.POST.get("codigo")
        codigo_generado=request.POST.get("validador")
        id_usuario=request.POST.get('id')
        rol_usuario=request.POST.get('rol')
        print("Código ingresado:", codigo_ingresado)
        if codigo_ingresado == codigo_generado :
            payload = {
                'id': id_usuario,
                'rol': rol_usuario,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            # Limpiar OTP después de usarlo
            return JsonResponse({
                'access': token,
                'usuario': {
                    'id': id_usuario,
                    'rol': rol_usuario
                }
            })
        else:
            return HttpResponse("Código incorrecto.", status=401)
    return JsonResponse({"error": "Método no permitido"}, status=405)

######################################################################################################################
@swagger_auto_schema(
    tags=['Calificacion'],
    method='post',
    operation_description="Crear una nueva calificación para un episodio.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idusuario', 'idepisodio', 'puntuacion', 'resenia'],
        properties={
            'idusuario': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
            'idepisodio': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del episodio'),
            'puntuacion': openapi.Schema(type=openapi.TYPE_INTEGER, description='Puntuación dada'),
            'resenia': openapi.Schema(type=openapi.TYPE_STRING, description='Reseña del usuario'),
        },
    ),
    responses={
        201: openapi.Response(description="Calificación enviada correctamente"),
        400: openapi.Response(description="Error al registrar calificación"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def crear_calificacion(request):
    if request.method=='POST':
        try:
            idusuario=request.POST.get('idusuario')
            idepisodio=request.POST.get('idepisodio')
            puntuacion=request.POST.get('puntuacion')
            resenia=request.POST.get('resenia')
            if not idusuario or not idepisodio or not puntuacion or not resenia:
                return JsonResponse({'error':'datos faltantes'})
            data = {
                'usuarios_idusuario':idusuario,
                'episodios_idepisodio':idepisodio,
                'puntuacion':puntuacion,
                'resenia':resenia,
            }
            response=supabase.table('calificacion').insert(data).execute()
            if hasattr(response, 'error') and response.error:
                return JsonResponse({'error': 'Error al registrar calificacion'}, status=400)
            return JsonResponse({'mensaje': 'Calificacion enviada'}, status=201) 
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    

######################################################################################################################
@swagger_auto_schema(
    tags=['Calificacion'],
    method='get',
    operation_description="Obtener calificaciones y reseñas de un episodio.",
    manual_parameters=[
        openapi.Parameter(
            name='episodios_idepisodio',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='ID del episodio a consultar',
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Reseñas obtenidas correctamente"),
        400: openapi.Response(description="Error al obtener reseñas"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def obtener_calificacion(request):
    if request.method=='GET':
        try:
            episodio=request.GET.get('episodios_idepisodio')
            response=supabase.table('calificacion').select('*','usuarios_idusuario(usuario)').eq('episodios_idepisodio',episodio).execute()
            if hasattr(response, 'error') and response.error:
                return JsonResponse({'error': 'Error al obtener reseñas'}, status=400)

            return JsonResponse({'resenias': response.data}, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
###################################################################################################################################
@swagger_auto_schema(
    tags=['Episodio'],
    method='get',
    operation_description="Obtener episodios recomendados basados en los creadores seguidos por el usuario.",
    manual_parameters=[
        openapi.Parameter(
            name='idusuario',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='ID del usuario que consulta',
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Episodios obtenidos exitosamente"),
        400: openapi.Response(description="Falta parámetro obligatorio"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
@token_required
def episodios(request):
    if request.method == 'GET':
        try:
            idUsuario = request.GET.get('idusuario')
            if not idUsuario:
                return JsonResponse({'error': 'Falta el parámetro idusuario'}, status=400)
            creadoresSeguidos = supabase.table('backend_listaseguidos').select('*').eq('usuarios_idusuario', idUsuario).execute()
            if not (hasattr(creadoresSeguidos, 'data') and creadoresSeguidos.data is not None):
                return JsonResponse({'error': 'Error al obtener creadores seguidos'}, status=500)
            if hasattr(creadoresSeguidos, 'error') and creadoresSeguidos.error:
                return JsonResponse({'error': str(creadoresSeguidos.error)}, status=500)
            creadores = [e['creadores_idcreador'] for e in creadoresSeguidos.data]
            obtenerCategoria = supabase.table('backend_podcast').select('categoria').in_('creadores_idcreador', creadores).execute()
            if not (hasattr(obtenerCategoria, 'data') and obtenerCategoria.data is not None):
                return JsonResponse({'error': 'Error al obtener categorías'}, status=500)
            if hasattr(obtenerCategoria, 'error') and obtenerCategoria.error:
                return JsonResponse({'error': str(obtenerCategoria.error)}, status=500)
            categorias = [e['categoria'] for e in obtenerCategoria.data]
            podcastsParaTi = supabase.table('backend_podcast').select('idpodcast').in_('categoria', categorias).execute()
            if not (hasattr(podcastsParaTi, 'data') and podcastsParaTi.data is not None):
                return JsonResponse({'error': 'Error al obtener podcasts'}, status=500)
            if hasattr(podcastsParaTi, 'error') and podcastsParaTi.error:
                return JsonResponse({'error': str(podcastsParaTi.error)}, status=500)
            ids_podcasts = [e['idpodcast'] for e in podcastsParaTi.data]
            episodiosParaTi = supabase.table('backend_episodios') \
                .select('*','podcast_idpodcast(*, creadores_idcreador(idcreador,nombre))') \
                .in_('podcast_idpodcast', ids_podcasts) \
                .eq('visible', True) \
                .order('fechapublicacion', desc=True) \
                .limit(10) \
                .execute()
            if not (hasattr(episodiosParaTi, 'data') and episodiosParaTi.data is not None):
                return JsonResponse({'error': 'Error al obtener episodios'}, status=500)
            if hasattr(episodiosParaTi, 'error') and episodiosParaTi.error:
                return JsonResponse({'error': str(episodiosParaTi.error)}, status=500)
            return JsonResponse({'episodios': episodiosParaTi.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
###################################################################################################################################################3
@swagger_auto_schema(
    tags=['Creador'],
    method='get',
    operation_description="Obtener el perfil de un creador por su ID.",
    manual_parameters=[
        openapi.Parameter(
            name='creadores_idcreador',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='ID del creador',
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Perfil del creador obtenido exitosamente"),
        400: openapi.Response(description="Falta el parámetro requerido"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
@token_required
def perfil_creador(request):
    if request.method == 'GET':
        try:
            # Obtener el parámetro usuarios_idusuario de la URL
            creadores_idcreador = request.GET.get('creadores_idcreador')
            print(creadores_idcreador)
            if not creadores_idcreador:
                return JsonResponse({'error': 'El parámetro creadores_idcreador es requerido'}, status=400)
            # Consultar la base de datos
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * 
                    FROM backend_creadores
                    WHERE idcreador = %s
                    """,
                    [creadores_idcreador]
                )
                columns = [col[0] for col in cursor.description]  # Nombres de las columnas
                creador = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            return JsonResponse({'creador': creador}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

##############################################################################################################################
@swagger_auto_schema(
    tags=['Usuario'],
    method='post',
    operation_description="Obtiene el perfil del usuario según su rol.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id', 'rol'],
        properties={
            'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID del usuario o creador'),
            'rol': openapi.Schema(type=openapi.TYPE_STRING, description='Rol del usuario: Administrador, Oyente o Creador'),
        },
    ),
    responses={
        200: "Perfil del usuario",
        400: "Faltan datos o ID inválido",
        404: "Usuario no encontrado",
        401: "Token inválido o faltante",
        500: "Error interno del servidor"
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])  # ❗ Desactiva autenticación
@permission_classes([AllowAny])
@token_required
def perfil_usuario(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id')
            rol = request.POST.get('rol')
            if not id or not rol:
                return JsonResponse({'error': 'Faltan datos requeridos'}, status=400)
            try:
                id_int = int(id)
            except ValueError:
                return JsonResponse({'error': 'id inválido'}, status=400)
            if rol in ['Administrador', 'Oyente']:
                response = supabase.table('backend_usuario').select('*').eq('idusuario', id_int).execute()
            else:
                response = supabase.table('backend_creadores').select('*').eq('idcreador', id_int).execute()
            if not response.data:
                return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
            usuario_data = response.data[0]
            if rol in ['Administrador', 'Oyente']:
                usuario = {
                    'id': usuario_data['idusuario'],
                    'usuario': usuario_data['usuario'],
                    'rol': usuario_data['rol'],
                    'correo': usuario_data['correo'],
                    'fecha': usuario_data['fecha_ingreso'],
                    'fotoperfil':usuario_data['fotoperfil']
                }
            else:
                usuario = {
                    'id': usuario_data['idcreador'],
                    'usuario': usuario_data['usuario'],
                    'nombre': usuario_data['nombre'],
                    'correo': usuario_data['correo'],
                    'rol': 'Creador',
                    'fotoPerfil': usuario_data['fotoperfil'],
                    'biografia': usuario_data['biografia'],
                    'donaciones': usuario_data['imgdonaciones']
                }
            return JsonResponse(usuario)
        except Exception as e:
            print(f"Error en perfil_usuario: {str(e)}")
            return JsonResponse({'error': 'Error en el servidor'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
#########################################################################################################################################
@swagger_auto_schema(
    tags=['Episodio'],
    method='get',
    operation_description="Obtener comentarios de un episodio específico.",
    manual_parameters=[
        openapi.Parameter(
            name='episodios_idepisodio',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='ID del episodio',
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Comentarios obtenidos correctamente"),
        400: openapi.Response(description="Error al consultar Supabase"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def obtenerComentarios(request):
    if request.method=='GET':
        try:
            idEpisodio=request.GET.get('episodios_idepisodio')
            response = supabase.table('backend_comentarios').select('*, usuarios_idusuario(usuario)').eq('episodios_idepisodio', idEpisodio).execute()
            if hasattr(response, 'error') and response.error:
                return JsonResponse({'error': 'Error al consultar Supabase'}, status=400)
            

            return JsonResponse({'comentarios': response.data}, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
####################################################################################################################################
@swagger_auto_schema(
    tags=['Episodio'],
    method='post',
    operation_description="Subir un nuevo comentario a un episodio.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idEpisodio', 'idOyente', 'contenido'],
        properties={
            'idEpisodio': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del episodio'),
            'idOyente': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del oyente (usuario)'),
            'contenido': openapi.Schema(type=openapi.TYPE_STRING, description='Contenido del comentario'),
        },
    ),
    responses={
        201: openapi.Response(description="Comentario enviado correctamente"),
        400: openapi.Response(description="Error al registrar en Supabase"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    
    security=[{'Bearer': []}]
)

@api_view(['POST'])
@authentication_classes([])  # ❗ Desactiva autenticación
@permission_classes([AllowAny])
def subir_comentarios(request):
    if request.method=='POST':
        try:
            idEpisodio=request.POST.get('idEpisodio')
            idOyente=request.POST.get('idOyente')
            contenido=request.POST.get('contenido')
            if not idEpisodio or not idOyente or not contenido:
                return JsonResponse({'error':'No hay datos para el comentario'})
            comentario = {
                'usuarios_idusuario':idOyente,
                'episodios_idepisodio':idEpisodio,
                'contenido':contenido,
            }
            response=supabase.table('backend_comentarios').insert(comentario).execute()
            if hasattr(response, 'error') and response.error:
                return JsonResponse({'error': 'Error al registrar en Supabase'}, status=400)
            return JsonResponse({'mensaje': 'Comentario enviado'}, status=201) 
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


#################################################################################################################################
@swagger_auto_schema(
    tags=['Buscar'],
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'q', openapi.IN_QUERY,
            description="Término de búsqueda (nombre, título o descripción)",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Resultados de búsqueda",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'creadores': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_OBJECT)
                    ),
                    'podcasts': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_OBJECT)
                    ),
                    'episodios': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_OBJECT)
                    ),
                }
            )
        ),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def buscar_general(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({
            'creadores': [],
            'podcasts': [],
            'episodios': []
        })
    try:
        # Buscar en creadores (filtramos por nombre Y username por separado)
        creadores1 = supabase.table('backend_creadores').select("*").ilike('nombre', f'%{query}%').execute()
        creadores2 = supabase.table('backend_creadores').select("*").ilike('usuario', f'%{query}%').execute()
        creadores = {c['idcreador']: c for c in (creadores1.data + creadores2.data)}.values()
        # Buscar en podcasts (por título y descripción)
        podcasts1 = supabase.table('backend_podcast').select("*").ilike('titulo', f'%{query}%').execute()
        podcasts2 = supabase.table('backend_podcast').select("*").ilike('descripcion', f'%{query}%').execute()
        podcasts = {p['idpodcast']: p for p in (podcasts1.data + podcasts2.data)}.values()
        # Buscar en episodios (por título y descripción)
        episodios1 = supabase.table('backend_episodios').select("*",'podcast_idpodcast(titulo, creadores_idcreador(nombre))').ilike('titulo', f'%{query}%').execute()
        episodios2 = supabase.table('backend_episodios').select("*",'podcast_idpodcast(titulo, creadores_idcreador(nombre))').ilike('descripcion', f'%{query}%').execute()
        episodios = {e['idepisodio']: e for e in (episodios1.data + episodios2.data)}.values()
        return JsonResponse({
            'creadores': list(creadores),
            'podcasts': list(podcasts),
            'episodios': list(episodios)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
########################################################################################################################
@swagger_auto_schema(
    tags=['Buscar'],
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'q', openapi.IN_QUERY,
            description="Año a buscar (formato: yyyy, por ejemplo: 2023)",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Resultados filtrados por año",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'creadores': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_OBJECT)
                    ),
                    'podcasts': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_OBJECT)
                    ),
                    'episodios': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_OBJECT)
                    ),
                }
            )
        ),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def buscar_anio (request):
    if request.method=='GET':
        anio=request.GET.get('q','').strip()
        if not anio:
            return JsonResponse({
                'creadores': [],
                'podcasts': [],
                'episodios': []
            })
        fecha_inicio = f"{anio}-01-01"
        fecha_fin = f"{int(anio)+1}-01-01"
        try:
            episodios = supabase.table('backend_episodios') .select("*",'podcast_idpodcast(titulo, creadores_idcreador(nombre))').gte('fechapublicacion', fecha_inicio).lt('fechapublicacion', fecha_fin).execute()
            podcasts=supabase.table('backend_podcast') .select("*").gte('fecha', fecha_inicio).lt('fecha', fecha_fin).execute()
            creadores=supabase.table('backend_creadores') .select("*").gte('fechaingreso', fecha_inicio).lt('fechaingreso', fecha_fin).execute()
            return JsonResponse({
                'creadores':creadores.data,
                'podcasts': podcasts.data,
                'episodios': episodios.data
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
###################################################################################################################################3    
@swagger_auto_schema(
    tags=['Buscar'],
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'q', openapi.IN_QUERY,
            description="Temática o categoría del podcast (ej: tecnología, salud, educación)",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Resultados filtrados por temática",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'creadores': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_OBJECT)
                    ),
                    'podcasts': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_OBJECT)
                    ),
                    'episodios': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_OBJECT)
                    ),
                }
            )
        ),
        500: openapi.Response(description="Error interno del servidor")
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def buscar_tematica(request):
    if request.method=='GET':
        tematica=request.GET.get('q','').strip()
        if not tematica:
            return JsonResponse({
                'creadores': [],
                'podcasts': [],
                'episodios': []
            })
        try:
           # Podcasts filtrados por categoría (temática)
            podcasts = supabase.table('backend_podcast')\
                .select('*')\
                .ilike('categoria', f'%{tematica}%')\
                .execute()
            idsP=supabase.table('backend_podcast').select('idpodcast').ilike('categoria',f'%{tematica}%').execute()
            idpodcasts = [p['idpodcast'] for p in idsP.data]
            # Episodios con info de podcast (incluye categoría), filtrados por categoría del podcast
            episodios = supabase.table('backend_episodios')\
                .select('*','podcast_idpodcast(titulo, creadores_idcreador(nombre))')\
                .in_('podcast_idpodcast', idpodcasts)\
                .execute()
            # Creadores con info de podcast (incluye categoría), filtrados por categoría del podcast
            idsC=supabase.table('backend_podcast').select('creadores_idcreador').ilike('categoria',f'%{tematica}%').execute()
            idCreadores=[c['creadores_idcreador'] for c in idsC.data]
            creadores = supabase.table('backend_creadores')\
                .select('*')\
                .in_('idcreador',idCreadores)\
                .execute()
            return JsonResponse({
                'creadores':creadores.data,
                'podcasts': podcasts.data,
                'episodios': episodios.data
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
#################################################################################################################################3
@swagger_auto_schema(
    tags=['Episodio'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idepisodio'],
        properties={
            'idepisodio': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="ID del episodio al que se le sumará una visualización"
            )
        }
    ),
    responses={
        200: openapi.Response(
            description="Visualización sumada correctamente",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'exito': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        400: openapi.Response(description="Error al sumar visualizaciones"),
        500: openapi.Response(description="Error interno del servidor")
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def sumar_visualizacion(request):
    if request.method=='POST':
        idEpisodio=request.POST.get('idepisodio')
        print('episodio= ',idEpisodio)
        if not idEpisodio:
            return JsonResponse({
                'error':'error al obtener episodio'
            })
        try:
            vistas = supabase.table('backend_episodios')\
                .select('visualizaciones')\
                .eq('idepisodio', idEpisodio)\
                .execute()
            visualizaciones_actuales = vistas.data[0]['visualizaciones'] if vistas.data else 0
            nuevas = visualizaciones_actuales + 1
            actualizar = supabase.table('backend_episodios')\
                .update({'visualizaciones': nuevas})\
                .eq('idepisodio', idEpisodio)\
                .execute()
            if hasattr(actualizar,'error')and actualizar.error:
                return JsonResponse({'error':'Error al sumar visualizaciones'})
            return JsonResponse({
                'exito': 'vistas aumentadas en 1'
            })
        except Exception as e:
            return JsonResponse({'error': 'error al actualizar visualizaciones'}, status=500)
            
#####################################################################################################################################
@swagger_auto_schema(
    tags=['Episodio'],
    method='post',
    manual_parameters=[],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['podcast', 'titulo', 'descripcion', 'fecha', 'audio'],
        properties={
            'podcast': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='ID del podcast al que pertenece el episodio'
            ),
            'titulo': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Título del episodio'
            ),
            'descripcion': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Descripción del episodio'
            ),
            'fecha': openapi.Schema(
                type=openapi.TYPE_STRING,
                format='date-time',
                example='2025-06-04T15:30',
                description='Fecha y hora de publicación (formato ISO, e.g., 2025-06-04T15:30)'
            ),
            'participantes': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Participantes del episodio (opcional)',
                default=''
            ),
            'audio': openapi.Schema(
                type=openapi.TYPE_FILE,
                description='Archivo de audio del episodio (.mp3, .aac, .m4a, .wav)'
            )
        }
    ),
    responses={
        201: openapi.Response(
            description="Episodio subido con éxito",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'mensaje': openapi.Schema(type=openapi.TYPE_STRING),
                    'audio_url': openapi.Schema(type=openapi.TYPE_STRING),
                    'fecha_publicacion': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        400: openapi.Response(description="Solicitud inválida o error en validación de datos"),
        500: openapi.Response(description="Error interno del servidor"),
        405: openapi.Response(description="Método no permitido")
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@token_required
def subir_episodio(request):
    if request.method == 'POST':
        try:
            # Validar campos obligatorios
            required_fields = ['podcast', 'titulo', 'descripcion', 'fecha']
            for field in required_fields:
                if field not in request.POST:
                    return JsonResponse({'error': f'Falta el campo requerido: {field}'}, status=400)
            # Obtener y formatear datos
            podcast = request.POST['podcast']
            titulo = request.POST['titulo'].strip()
            descripcion = request.POST['descripcion'].strip()
            fecha_str = request.POST['fecha']
            participantes = request.POST.get('participantes', '')
            print(podcast)
            print(titulo)
            print(descripcion)
            print(fecha_str)
            print(participantes)
            # Convertir y validar fecha
            try:
                fecha_hora = datetime.datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M")
                fecha_hora = timezone.make_aware(fecha_hora)
                fecha_iso = fecha_hora.isoformat()  # Convertir a string ISO
            except ValueError:
                return JsonResponse({'error': 'Formato de fecha inválido. Use YYYY-MM-DDTHH:MM'}, status=400)
            # Determinar visibilidad
            visible = timezone.now() >= fecha_hora
            # Validar archivo de audio
            if 'audio' not in request.FILES:
                return JsonResponse({'error': 'No se proporcionó archivo de audio'}, status=400)
            audio = request.FILES['audio']
            allowed_extensions = ['.mp3', '.aac', '.m4a', '.wav']
            file_extension = os.path.splitext(audio.name)[1].lower()
            if file_extension not in allowed_extensions:
                return JsonResponse({
                    'error': 'Formato de audio no permitido',
                    'formatos_aceptados': allowed_extensions
                }, status=400)
            # Subir audio a Supabase
            audio_nombre = f'audio_{titulo}_{podcast}_{uuid.uuid4().hex}{file_extension}'
            nombre_audio_seguro = audio_nombre.replace(' ', '_')
            camino = f"episodios/{nombre_audio_seguro}"
            try:
                upload_response = supabase.storage.from_('audios').upload(
                    path=camino,
                    file=audio.read(),
                    file_options={
                        "content-type": audio.content_type,
                        "upsert": False
                    }
                )
                audio_url = supabase.storage.from_('audios').get_public_url(camino)
            except Exception as upload_error:
                return JsonResponse({'error': f'Error al subir audio: {str(upload_error)}'}, status=500)
            # Preparar datos para Supabase (convertir datetime a string ISO)
            episodio_data = {
                "podcast_idpodcast": podcast,
                "titulo": titulo,
                "descripcion": descripcion,
                "fechapublicacion": fecha_iso,  # Usamos el string ISO en lugar del objeto datetime
                "audio": audio_url,
                "participantes": participantes,
                "visible": visible
            }
            # Insertar en la base de datos
            response = supabase.table('backend_episodios').insert(episodio_data).execute()
            if hasattr(response, 'error') and response.error:
                # Intentar eliminar el audio subido si falla la inserción
                try:
                    supabase.storage.from_('audios').remove([camino])
                except:
                    pass
                return JsonResponse({'error': str(response.error)}, status=400)
            return JsonResponse({
                'mensaje': 'Episodio subido con éxito',
                'audio_url': audio_url,
                'fecha_publicacion': fecha_iso
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
###################################################################################################################################
@swagger_auto_schema(
    tags=['Podcast'],
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'idcreador',
            openapi.IN_QUERY,
            description='ID del creador para filtrar podcasts',
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Lista de podcasts filtrados por creador",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'podcasts': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT)
                    )
                }
            )
        ),
        500: openapi.Response(description="Error en el servidor")
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
@token_required
def podcasts_por_creador(request):
    if request.method == 'GET':
        try:
            id_creador = request.GET.get('idcreador')
            response = supabase.table('backend_podcast')\
                               .select('*')\
                               .eq('creadores_idcreador', id_creador)\
                               .execute()
            podcasts = response.data or []

            return JsonResponse({'podcasts': podcasts}, status=200)

        except Exception as e:
            print(f"Error en obtener podcasts: {str(e)}")
            return JsonResponse({'error': 'Error en el servidor'}, status=500)
##########################################################################################################################
@swagger_auto_schema(
    tags=['Podcast'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['creador', 'titulo', 'descripcion', 'categoria'],
        properties={
            'creador': openapi.Schema(type=openapi.TYPE_STRING, description='ID del creador'),
            'titulo': openapi.Schema(type=openapi.TYPE_STRING, description='Título del podcast'),
            'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del podcast'),
            'categoria': openapi.Schema(type=openapi.TYPE_STRING, description='Categoría del podcast'),
            'premium': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indica si es premium', default=False),
        }
    ),
    responses={
        201: openapi.Response(description="Podcast creado con éxito"),
        400: openapi.Response(description="Error al registrar en Supabase"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def crear_podcast(request):
    if request.method=='POST':
        try:
            creador=request.POST.get('creador')
            titulo=request.POST.get('titulo')
            descripcion=request.POST.get('descripcion')
            categoria=request.POST.get('categoria')
            premium=request.POST.get('premium','false')
            premium=premium=='true'

            data = {
                "creadores_idcreador":creador,
                "titulo":titulo,
                "descripcion":descripcion,
                "categoria":categoria,
                "premium":premium,
            }
            response = supabase.table('backend_podcast').insert(data).execute()
            if hasattr(response, 'error') and response.error:
                return JsonResponse({'error': 'Error al registrar en Supabase'}, status=400)
            return JsonResponse({'mensaje': 'Podcast creado con éxito'}, status=201) 
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
#########################################################################################################################
@swagger_auto_schema(
    tags=['Usuario'],
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'usuarios_idusuario',
            openapi.IN_QUERY,
            description='ID del usuario para obtener sus seguimientos',
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Lista de creadores que sigue el usuario",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'siguiendo': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'usuarios_idusuario': openapi.Schema(type=openapi.TYPE_STRING),
                                'creadores_idcreador': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    )
                }
            )
        ),
        400: openapi.Response(description="Parámetro requerido faltante"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error en el servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
@token_required
def obtenerSeguimientos(request):
    if request.method == 'GET':
        try:
            # Obtener el parámetro usuarios_idusuario de la URL
            usuarios_idusuario = request.GET.get('usuarios_idusuario')
            if not usuarios_idusuario:
                return JsonResponse({'error': 'El parámetro usuarios_idusuario es requerido'}, status=400)
            # Consultar la base de datos
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT usuarios_idusuario, creadores_idcreador 
                    FROM backend_listaseguidos
                    WHERE usuarios_idusuario = %s
                    """,
                    [usuarios_idusuario]
                )
                columns = [col[0] for col in cursor.description]  # Nombres de las columnas
                seguimientos = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            return JsonResponse({'siguiendo': seguimientos}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
####################################################################################################################3
@swagger_auto_schema(
    tags=['Usuario'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['usuarios_idusuario', 'creadores_idcreador'],
        properties={
            'usuarios_idusuario': openapi.Schema(type=openapi.TYPE_STRING, description='ID del usuario que sigue'),
            'creadores_idcreador': openapi.Schema(type=openapi.TYPE_STRING, description='ID del creador a seguir'),
        }
    ),
    responses={
        201: openapi.Response(description="Seguimiento registrado con éxito"),
        400: openapi.Response(description="Faltan campos requeridos"),
        500: openapi.Response(description="Error interno del servidor"),
    },security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def seguirCreador(request):
    if request.method == 'POST':
        try:
            usuarios_idusuario = request.POST.get('usuarios_idusuario')
            creadores_idcreador = request.POST.get('creadores_idcreador')
            if not usuarios_idusuario or not creadores_idcreador:
                return JsonResponse({'error': 'Faltan campos requeridos'}, status=400)
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO backend_listaseguidos 
                    (usuarios_idusuario, creadores_idcreador)
                    VALUES (%s, %s)
                    RETURNING creadores_idcreador
                    """,
                    [usuarios_idusuario, creadores_idcreador]
                )
                new_id = cursor.fetchone()[0]
                return JsonResponse({
                    'usuarios_idusuario': usuarios_idusuario,
                    'creadores_idcreador': creadores_idcreador
                }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
#########################################################################################################################
@swagger_auto_schema(
    tags=['Usuario'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idusuario', 'idcreador'],
        properties={
            'idusuario': openapi.Schema(type=openapi.TYPE_STRING, description='ID del usuario que dejará de seguir'),
            'idcreador': openapi.Schema(type=openapi.TYPE_STRING, description='ID del creador que será dejado de seguir'),
        },
    ),
    responses={
        201: openapi.Response(description='Se dejó de seguir al creador correctamente'),
        400: openapi.Response(description='Datos faltantes o error al registrar en Supabase'),
        500: openapi.Response(description='Error interno del servidor'),
    },
    security=[{'Bearer': []}]

)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def dejarSeguirCreador(request):
    if request.method == 'POST':
        try:
            idusuario = request.POST.get('idusuario')
            idcreador = request.POST.get('idcreador')
            print(f"idusuario: {idusuario}, idcreador: {idcreador}")  # <-- imprime los datos

            if not idusuario or not idcreador:
                return JsonResponse({'error': 'Datos faltantes'}, status=400)

            response = supabase.table('backend_listaseguidos') \
                               .delete() \
                               .eq('usuarios_idusuario', idusuario) \
                               .eq('creadores_idcreador', idcreador) \
                               .execute()

            print(f"Response: {response}")  # <-- imprime la respuesta

            if hasattr(response, 'error') and response.error:
                return JsonResponse({'error': 'Error al registrar en Supabase'}, status=400)

            return JsonResponse({'mensaje': 'Se dejo de seguir al creador'}, status=201)
        except Exception as e:
            print(f"Excepción: {str(e)}")  # <-- imprime el error exacto
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
#########################################################################################################################



def mostrar_creadores(request):
    try:    
        # 1. Configuración Supabase
        supabase_url = url
        supabase_key = key
        storage_url = f"{supabase_url}/storage/v1/object/public"
        if not supabase_url or not supabase_key:
            logger.error("Missing Supabase credentials")
            raise ValueError("Configuración de Supabase no encontrada")
        # 2. Conexión a Supabase
        supabase = create_client(supabase_url, supabase_key)
        # 3. Obtener datos
        try:
            response = supabase.table('backend_creadores').select('*').execute()
            creadores = response.data if hasattr(response, 'data') else []
        except Exception as query_error:
            logger.error(f"Error en consulta Supabase: {str(query_error)}")
            creadores = []
        # 4. Procesar URLs de imágenes
        processed_creadores = []
        for creador in creadores:
            # Construir URLs completas para imágenes
            fotoperfil = (
                f"{storage_url}/fotperfiles/{creador['fotoperfil'].split('/')[-1]}" 
                if creador.get('fotoperfil') 
                else None
            )
            imgdonaciones = (
                f"{storage_url}/fotoqr/{creador['imgdonaciones'].split('/')[-1]}" 
                if creador.get('imgdonaciones') 
                else None
            )
            processed_creadores.append({
                'usuario': creador.get('usuario', 'Anónimo'),
                'correo': creador.get('correo', ''),
                'biografia': creador.get('biografia', ''),
                'fotoperfil': fotoperfil,
                'imgdonaciones': imgdonaciones
            })
        # 5. Renderizar template
        return render(request, 'creadores/lista.html', {
            'creadores': processed_creadores,
            'titulo': 'Listado de Creadores',
            'current_time': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'debug_mode': DEBUG
        })

    except Exception as e:
        logger.exception("Error en mostrar_creadores")
        return render(request, 'error.html', {
            'error_message': "Disculpe las molestias. Estamos trabajando para solucionar el problema."
        }, status=500)


#########################################################################################################################
@swagger_auto_schema(
    tags=['Creador'],
    method='post',
    manual_parameters=[],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['usuario', 'contrasenia', 'nombre', 'correo'],
        properties={
            'usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de usuario'),
            'contrasenia': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del creador'),
            'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre completo del creador'),
            'correo': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='Correo electrónico'),
            'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Número de teléfono'),
            'biografia': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción biográfica'),
            'fotoperfil': openapi.Schema(type=openapi.TYPE_FILE, description='Foto de perfil (imagen JPG/PNG)'),
            'imgdonaciones': openapi.Schema(type=openapi.TYPE_FILE, description='Imagen QR de donaciones'),
        }
    ),
    responses={
        200: openapi.Response(description="Registro exitoso"),
        400: openapi.Response(description="Error en los datos o al subir archivos"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def registro_creador(request):
    if request.method == 'POST':
        try:
            # 1. Obtener datos del formulario
            usuario = request.POST.get('usuario')
            contrasenia = request.POST.get('contrasenia')
            nombre = request.POST.get('nombre')
            correo = request.POST.get('correo')
            telefono=request.POST.get('telefono')
            biografia = request.POST.get('biografia')

            # 2. Procesar archivos (foto de perfil y QR de donaciones)
            fotoperfil = None
            if 'fotoperfil' in request.FILES:
                fotoperfil = request.FILES['fotoperfil']
                try:
                    # Subir a Supabase Storage
                    foto_perfil_name = f'perfil_{usuario}_{uuid.uuid4().hex}.jpg'
                    supabase.storage.from_('fotperfiles').upload(
                        path=foto_perfil_name,
                        file=fotoperfil.read(),
                    )
                    fotoperfil = supabase.storage.from_('fotperfiles').get_public_url(foto_perfil_name)
                except Exception as e:
                    return JsonResponse({'error': f'Error al subir foto de perfil: {str(e)}'}, status=400)

            imgdonaciones = None
            if 'imgdonaciones' in request.FILES:
                imgdonaciones = request.FILES['imgdonaciones']
                try:
                    # Subir a Supabase Storage
                    img_qr_name = f'donaciones_{usuario}_{uuid.uuid4().hex}.png'
                    supabase.storage.from_('fotoqr').upload(
                        path=img_qr_name,
                        file=imgdonaciones.read(),
                    )
                    imgdonaciones = supabase.storage.from_('fotoqr').get_public_url(img_qr_name)
                except Exception as e:
                    return JsonResponse({'error': f'Error al subir QR de donaciones: {str(e)}'}, status=400)

            # 3. Hashear contraseña
            contrasenia_hash = make_password(contrasenia)

            # 4. Insertar en la tabla de creadores
            data = {
                "usuario": usuario,
                "contrasenia": contrasenia_hash,
                "nombre": nombre,
                "correo": correo,
                "biografia": biografia,
                "fotoperfil": fotoperfil,
                "imgdonaciones": imgdonaciones,
                "telefono":telefono
            }
            
            response = supabase.table('backend_creadores').insert(data).execute()

            # 5. Verificar si hubo errores
            if hasattr(response, 'error') and response.error:
                return JsonResponse({'error': 'Error al registrar en Supabase'}, status=400)

            # 6. Éxito: Redirigir o devolver éxito
            return JsonResponse( {"message": "¡Registro exitoso!"})
        except Exception as e:
            # Captura cualquier error inesperado y devuelve un mensaje genérico
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

#########################################################################################################################
@swagger_auto_schema(
    tags=['Usuario'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['usuario', 'contrasenia', 'tipoUsuario', 'correo', 'telefono'],
        properties={
            'usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de usuario'),
            'contrasenia': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del usuario'),
            'tipoUsuario': openapi.Schema(type=openapi.TYPE_STRING, description='Rol del usuario (ej. creador, seguidor)'),
            'correo': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='Correo electrónico'),
            'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Número de teléfono'),
            'fotoPerfil': openapi.Schema(type=openapi.TYPE_FILE, description='Foto de perfil del usuario (JPG/PNG)'),
        }
    ),
    responses={
        201: openapi.Response(description='Usuario creado con éxito'),
        400: openapi.Response(description='Error en los datos enviados o al subir imagen'),
        500: openapi.Response(description='Error interno del servidor'),
    }
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def registro_usuario(request):
    if request.method == 'POST':
        try:
            usuario=request.POST.get('usuario')
            contrasenia=request.POST.get('contrasenia')
            rol=request.POST.get('tipoUsuario')
            correo=request.POST.get('correo')
            telefono=request.POST.get('telefono')
            fecha=timezone.now().date().isoformat()
            contrasenia_hash=make_password(contrasenia)
            fotoperfil = None
            if 'fotoPerfil' in request.FILES:
                fotoperfil = request.FILES['fotoPerfil']
                try:
                    # Subir a Supabase Storage
                    foto_perfil_name = f'perfil_{usuario}_{uuid.uuid4().hex}.jpg'
                    supabase.storage.from_('fotosusuarios').upload(
                        path=foto_perfil_name,
                        file=fotoperfil.read(),
                    )
                    fotoperfilstr = supabase.storage.from_('fotosusuarios').get_public_url(foto_perfil_name)
                except Exception as e:
                    return JsonResponse({'error': f'Error al subir foto de perfil: {str(e)}'}, status=400)
            data = {
                "usuario":usuario,
                "contrasenia":contrasenia_hash,
                "rol":rol,
                "correo":correo,
                "fecha_ingreso":fecha,
                "fotoperfil":fotoperfilstr,
                "telefono":telefono
            }
            response = supabase.table('backend_usuario').insert(data).execute()
            if hasattr(response, 'error') and response.error:
                return JsonResponse({'error': 'Error al registrar en Supabase'}, status=400)
            return JsonResponse({'mensaje': 'Usuario creado con éxito'}, status=201) 
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

#########################################################################################################################
@swagger_auto_schema(
    tags=['Usuario'],
    method='get',
    operation_description="Lista todos los usuarios registrados en la base de datos.",
    responses={
        200: openapi.Response(description='Lista de usuarios obtenida con éxito'),
        500: openapi.Response(description='Error de conexión o error al consultar los datos')
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def listar_usuarios(request):
    """Vista para listar todos los usuarios (GET)."""
    conn = obtener_conexion()
    if not conn:
        return JsonResponse({'error': 'Error de conexión'}, status=500)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM backend_usuario;")
            usuarios = cursor.fetchall()
            # Convertir resultados a JSON
            column_names = [desc[0] for desc in cursor.description]
            usuarios_json = [
                dict(zip(column_names, row))
                for row in usuarios
            ]
            return JsonResponse({'usuarios': usuarios_json}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        conn.close()


#########################################################################################################################
@swagger_auto_schema(
    tags=['Creador'],
    method='get',
    operation_description='Obtiene la lista de todos los creadores registrados en la plataforma.',
    responses={
        200: openapi.Response(
            description="Lista de creadores obtenida exitosamente",
            examples={
                "application/json": {
                    "creadores": [
                        {
                            "idcreador": 1,
                            "usuario": "creador1",
                            "nombre": "Nombre Creador",
                            "correo": "correo@example.com",
                            "biografia": "Texto de biografía",
                            "fotoperfil": "https://...",
                            "imgdonaciones": "https://...",
                            "telefono": "71234567"
                        }
                    ]
                }
            }
        ),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def listar_creadores(request):
    """Vista para listar todos los creadores (GET)."""
    conn = obtener_conexion()
    if not conn:
        return JsonResponse({'error': 'Error de conexión'}, status=500)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM backend_creadores;")
            creadores = cursor.fetchall()
            
            # Convertir resultados a JSON
            column_names = [desc[0] for desc in cursor.description]
            creadores_json = [
                dict(zip(column_names, row))
                for row in creadores
            ]
            
            return JsonResponse({'creadores': creadores_json}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        conn.close()
#########################################################################################################################

##PARA EL DASHBOARD DE CREADORES
@swagger_auto_schema(
    method='get',
    tags=['Creador'],
    operation_description='Obtiene la cantidad total de visualizaciones de todos los episodios del creador.',
    manual_parameters=[],
    request_body=None,
    responses={
        200: openapi.Response(
            description="Cantidad total de visualizaciones del creador",
            examples={
                "application/json": {
                    "Vistas del creador": 1234
                }
            }
        ),
        400: openapi.Response(description="Error al obtener visualizaciones"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def obtener_visualizaciones(request):
    if request.method=='GET':
        try:
            idcreador=request.GET.get('idcreador')
            podcasts=supabase.table('backend_podcast').select('idpodcast').eq('creadores_idcreador',idcreador).execute()
            arreglo_podcasts=[podcast['idpodcast']for podcast in podcasts.data]
            print(arreglo_podcasts)
            response=supabase.table('backend_episodios').select('visualizaciones').in_('podcast_idpodcast',arreglo_podcasts).execute()
            if hasattr(response, 'error') and response.error:
                return JsonResponse({'error': 'Error al obtener visualizaciones'}, status=400)
            episodios=response.data
            suma_vistas = sum(episodio["visualizaciones"] for episodio in episodios)
            return JsonResponse({'Vistas del creador': suma_vistas})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

#########################################################################################################################
@swagger_auto_schema(
    method='get',
    tags=['Episodio'],
    operation_description='Obtiene el episodio más visto de todos los podcasts de un creador.',
    manual_parameters=[
        openapi.Parameter(
            'idcreador',
            openapi.IN_QUERY,
            description="ID del creador",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Episodio más visto",
            examples={
                "application/json": {
                    "episodio mas visto": {
                        "idepisodio": 7,
                        "titulo": "Mi gran episodio",
                        "visualizaciones": 456,
                        "podcast_idpodcast": 3
                    }
                }
            }
        ),
        400: openapi.Response(description="Error al obtener episodio más visto"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def obtener_ep_mas_visto(request):
    if request.method=='GET':
        try:
            idcreador=request.GET.get('idcreador')
            podcasts=supabase.table('backend_podcast').select('idpodcast').eq('creadores_idcreador',idcreador).execute()
            arreglo_podcasts=[podcast['idpodcast']for podcast in podcasts.data]
            res = supabase.table("backend_episodios").select("*").in_('podcast_idpodcast',arreglo_podcasts).order("visualizaciones", desc=True).limit(1).execute()
            if hasattr(res, 'error') and res.error:
                return JsonResponse({'error': 'Error al obtener epidosio más visto'}, status=400)
            return JsonResponse({'episodio mas visto':res.data[0]})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
#########################################################################################################################
@swagger_auto_schema(
    method='get',
    tags=['Creador'],
    operation_description='Obtiene la cantidad total de seguidores que tiene un creador.',
    manual_parameters=[
        openapi.Parameter(
            name='idcreador',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=True,
            description='ID del creador del que se desea obtener el conteo de seguidores.'
        ),
    ],
    responses={
        200: openapi.Response(
            description="Cantidad de seguidores del creador",
            examples={
                "application/json": {
                    "Cantidad de seguidores": 128
                }
            }
        ),
        400: openapi.Response(description="Error al obtener conteo de seguidores"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def obtenerSeguidores(request):
    if request.method=='GET':
        try:
            idcreador=request.GET.get('idcreador')
            seguidores=supabase.table('backend_listaseguidos').select('*',count="exact").eq('creadores_idcreador',idcreador).execute()
            if hasattr(seguidores, 'error') and seguidores.error:
                return JsonResponse({'error': 'Error al obtener conteo de seguidores'}, status=400)
            conteo=seguidores.count
            return JsonResponse({'Cantidad de seguidores':conteo})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


#########################################################################################################################


##endpoints nuevos
@swagger_auto_schema(
    method='post',
    tags=['Usuario'],
    operation_description='Permite hacer una donación a un creador específico.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idcreador', 'monto'],
        properties={
            'idcreador': openapi.Schema(type=openapi.TYPE_STRING, description='ID del creador a quien se dona'),
            'monto': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', description='Monto de la donación')
        }
    ),
    responses={
        200: openapi.Response(description="Donación completada exitosamente", examples={"application/json": {"mensaje": "Donacion completa"}}),
        400: openapi.Response(description="Error al actualizar recaudado o datos incorrectos"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def donarCreador(request):
    if request.method=='POST':
        try:
            idcreador=request.POST.get('idcreador')
            monto=request.POST.get('monto')
            monto = float(monto) 
            recaudado=supabase.table('backend_creadores').select('recaudado').eq('idcreador',idcreador).execute()
            recaudadoActual = recaudado.data[0]['recaudado'] if recaudado.data else 0
            nuevas = recaudadoActual + monto
            actualizar = supabase.table('backend_creadores')\
                .update({'recaudado': nuevas})\
                .eq('idcreador', idcreador)\
                .execute()
            if hasattr(actualizar, 'error') and actualizar.error:
                return JsonResponse({'error': 'Error al actualizar recaudado'}, status=400)
            return JsonResponse({'mensaje':'Donacion completa'})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


    #########################################################################################################################
@swagger_auto_schema(
    method='post',
    tags=['Lista Reproduccion'],
    operation_description='Crear una nueva lista de reproducción para un usuario.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idusuario', 'tituloLista'],
        properties={
            'idusuario': openapi.Schema(type=openapi.TYPE_STRING, description='ID del usuario'),
            'tituloLista': openapi.Schema(type=openapi.TYPE_STRING, description='Título de la lista de reproducción')
        }
    ),
    responses={
        200: openapi.Response(description="Lista creada exitosamente", examples={"application/json": {"mensaje": "lista creada"}}),
        400: openapi.Response(description="Datos faltantes o error al crear la lista"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def crearListaReproduccion(request):
    if request.method=='POST':
        try:
            idusuario=request.POST.get('idusuario')
            titulo=request.POST.get('tituloLista')
            if not idusuario or not titulo:
                return JsonResponse({'error': 'Datos faltantes'}, status=400)
            data={
                "usuarios_idusuario":idusuario,
                "titulo":titulo
            }
            lista=supabase.table('listareproduccion').insert(data).execute()
            if hasattr(lista, 'error') and lista.error:
                return JsonResponse({'error': 'Error al crear lista de reproduccion'}, status=400)
            return JsonResponse({'mensaje':'lista creada'})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
#########################################################################################################################
@swagger_auto_schema(
    method='post',
    tags=['Lista Reproduccion'],
    operation_description='Agregar un episodio a una lista de reproducción.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idepisodio', 'idLista'],
        properties={
            'idepisodio': openapi.Schema(type=openapi.TYPE_STRING, description='ID del episodio'),
            'idLista': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la lista de reproducción'),
        },
    ),
    responses={
        200: openapi.Response(description="Episodio agregado a la lista"),
        400: openapi.Response(description="Datos faltantes o error en la operación"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def agregarEpisodioLista(request):
    if request.method=='POST':
        try:
            episodio=request.POST.get('idepisodio')
            lista=request.POST.get('idLista')
            if not episodio or not lista:
                return JsonResponse({'error': 'Datos faltantes'}, status=400)
            data={
                "episodios_idepisodio":episodio,
                "listareproduccion_idlista":lista
            }
            agregado=supabase.table('episodioslista').insert(data).execute()
            if hasattr(agregado, 'error') and agregado.error:
                return JsonResponse({'error': 'Error al agregar episodio a lista'}, status=400)
            return JsonResponse({'mensaje':'episodio agregado a lista'})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
#########################################################################################################################
@swagger_auto_schema(
    method='post',
    tags=['Lista Reproduccion'],
    operation_description='Eliminar un episodio de una lista de reproducción.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idepisodio', 'idLista'],
        properties={
            'idepisodio': openapi.Schema(type=openapi.TYPE_STRING, description='ID del episodio'),
            'idLista': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la lista de reproducción')
        }
    ),
    responses={
        200: openapi.Response(description="Episodio eliminado de la lista"),
        400: openapi.Response(description="Datos faltantes o error al borrar episodio"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def quitarEpisodio(request):
    if request.method=='POST':
        try:
            episodio=request.POST.get('idepisodio')
            lista=request.POST.get('idLista')
            if not episodio or not lista:
                return JsonResponse({'error': 'Datos faltantes'}, status=400)
            borrado=supabase.table('episodioslista').delete().eq('episodios_idepisodio',episodio).eq('listareproduccion_idlista',lista).execute()
            if hasattr(borrado, 'error') and borrado.error:
                return JsonResponse({'error': 'Error al borrar episodio de lista'}, status=400)
            return JsonResponse({'mensaje':'episodio eliminado de lista'})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

#########################################################################################################################
@swagger_auto_schema(
    method='post',
    tags=['Comentario'],
    operation_description='Eliminar un comentario por su ID.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idcomentario'],
        properties={
            'idcomentario': openapi.Schema(type=openapi.TYPE_STRING, description='ID del comentario a eliminar'),
        },
    ),
    responses={
        200: openapi.Response(description="Comentario eliminado correctamente"),
        400: openapi.Response(description="Datos faltantes o error al eliminar"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def borrarComentario(request):
    if request.method=='POST':
        try:
            idcomentario=request.POST.get('idcomentario')
            if not idcomentario:
                return JsonResponse({'error': 'Datos faltantes'}, status=400)
            comentarioBorrado=supabase.table('backend_comentarios').delete().eq('idcomentario',idcomentario).execute()
            if hasattr(comentarioBorrado, 'error') and comentarioBorrado.error:
                return JsonResponse({'error': 'Error al borrar comentario'}, status=400)
            return JsonResponse({'mensaje':'comentario eliminado'})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

#########################################################################################################################
@swagger_auto_schema(
    method='post',
    tags=['Episodio'],
    operation_description='Borra un episodio y todos sus datos relacionados (comentarios, calificaciones, listas, audio).',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idepisodio'],
        properties={
            'idepisodio': openapi.Schema(type=openapi.TYPE_STRING, description='ID del episodio a borrar'),
        },
    ),
    responses={
        200: openapi.Response(description='Episodio eliminado correctamente'),
        400: openapi.Response(description='Error de validación o eliminación'),
        500: openapi.Response(description='Error interno del servidor'),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def borrarEpisodio(request):
    if request.method=='POST':
        try:
            idEpisodio=request.POST.get('idepisodio')
            comentarios=supabase.table('backend_comentarios').delete().eq('episodios_idepisodio',idEpisodio).execute()
            if hasattr(comentarios, 'error') and comentarios.error:
                return JsonResponse({'error': 'Error al borrar comentarios'}, status=400)
            calificacion=supabase.table('calificacion').delete().eq('episodios_idepisodio',idEpisodio).execute()
            if hasattr(calificacion, 'error') and calificacion.error:
                return JsonResponse({'error': 'Error al borrar calificacion'}, status=400)
            listaEpisodio=supabase.table('episodioslista').delete().eq('episodios_idepisodio',idEpisodio).execute()
            if hasattr(listaEpisodio,'erro') and listaEpisodio.error:
                return JsonResponse({'error':'error al borrar episodios de listas'})
            audio=supabase.table('backend_episodios').select('*').eq('idepisodio',idEpisodio).execute()
            if hasattr(audio,'error')and audio.error:
                return JsonResponse({'error':'error al obtener el audio del episodio'})
            episodio=supabase.table('backend_episodios').delete().eq('idepisodio',idEpisodio).execute()
            if hasattr(episodio, 'error') and  episodio.error:
                return JsonResponse({'error': 'Error al borrar episodio'}, status=400) 
            ruta = audio.data[0]['audio']  # suponiendo que siempre hay 1 resultado
            if ruta:
                delete_result = supabase.storage.from_('audios').remove([ruta])
                if hasattr(delete_result, 'error') and delete_result.error:
                    return JsonResponse({'error': 'Episodio borrado, pero error al borrar archivo del bucket'}, status=500)
            return JsonResponse({'mensaje':'Episodio eliminado'})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

def obtener_ruta_relativa(url_completa):
                try:
                    return url_completa.split('/audios/')[1]
                except IndexError:
                    return None
                
#########################################################################################################################
@swagger_auto_schema(
    method='post',
    tags=['Podcast'],
    operation_description='Elimina un podcast y todos los datos relacionados: episodios, comentarios, calificaciones, suscripciones y listas.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idpodcast'],
        properties={
            'idpodcast': openapi.Schema(type=openapi.TYPE_STRING, description='ID del podcast a eliminar'),
        },
    ),
    responses={
        200: openapi.Response(description='Podcast eliminado correctamente'),
        400: openapi.Response(description='Error en la validación o eliminación'),
        500: openapi.Response(description='Error interno del servidor'),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def borrarPodcast(request):
    if request.method=='POST':
        try:
            idpodcast=request.POST.get('idpodcast')
            episodios=supabase.table('backend_episodios').select('idepisodio').eq('podcast_idpodcast',idpodcast).execute()
            idepisodios = [e['idepisodio'] for e in episodios.data]
            comentarios=supabase.table('backend_comentarios').delete().in_('episodios_idepisodio',idepisodios).execute()
            if hasattr(comentarios, 'error') and comentarios.error:
                return JsonResponse({'error': 'Error al borrar comentarios'}, status=400)
            calificacion=supabase.table('calificacion').delete().in_('episodios_idepisodio',idepisodios).execute()
            if hasattr(calificacion, 'error') and calificacion.error:
                return JsonResponse({'error': 'Error al borrar calificacion'}, status=400)
            episodioslistas=supabase.table('episodioslista').delete().in_('episodios_idepisodio',idepisodios).execute()
            if hasattr(episodioslistas, 'error') and  episodioslistas.error:
                return JsonResponse({'error': 'Error al borrar episodio de lista de reproduccion'}, status=400)     
            episodios=supabase.table('backend_episodios').delete().eq('podcast_idpodcast',idpodcast).execute()
            if hasattr(episodios, 'error') and  episodios.error:
                return JsonResponse({'error': 'Error al borrar episodios'}, status=400) 
            suscripcion=supabase.table('suscripcion').delete().eq('podcast_idpodcast',idpodcast).execute()
            if hasattr(suscripcion, 'error') and suscripcion.error:
                return JsonResponse({'error': 'Error al borrar suscripcion'}, status=400)
            podcast=supabase.table('backend_podcast').delete().eq('idpodcast',idpodcast).execute()
            if hasattr(podcast, 'error') and podcast.error:
                return JsonResponse({'error': 'Error al borrar podcast'}, status=400)
            return JsonResponse({'mensaje':'podcast eliminado'})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
   #########################################################################################################################
@swagger_auto_schema(
    method='post',
    tags=['Creador'],
    operation_description='Elimina un creador y todos sus datos relacionados: podcasts, episodios, comentarios, calificaciones, listas, suscripciones y seguidos.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idcreador'],
        properties={
            'idcreador': openapi.Schema(type=openapi.TYPE_STRING, description='ID del creador a eliminar'),
        },
    ),
    responses={
        200: openapi.Response(description='Creador eliminado correctamente'),
        400: openapi.Response(description='Error en alguna operación de eliminación'),
        500: openapi.Response(description='Error interno del servidor'),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def borrarCreador(request):
    if request.method=='POST':
        try:
            idCreador=request.POST.get('idcreador')
            podcasts=supabase.table('backend_podcast').select('idpodcast').eq('creadores_idcreador',idCreador).execute()
            idpodcasts = [e['idpodcast'] for e in podcasts.data]
            episodios=supabase.table('backend_episodios').select('idepisodio').in_('podcast_idpodcast',idpodcasts).execute()
            idepisodios = [e['idepisodio'] for e in episodios.data]
            comentarios=supabase.table('backend_comentarios').delete().in_('episodios_idepisodio',idepisodios).execute()
            if hasattr(comentarios, 'error') and comentarios.error:
                return JsonResponse({'error': 'Error al borrar comentarios'}, status=400)
            calificacion=supabase.table('calificacion').delete().in_('episodios_idepisodio',idepisodios).execute()
            if hasattr(calificacion, 'error') and calificacion.error:
                return JsonResponse({'error': 'Error al borrar calificacion'}, status=400)
            episodioslistas=supabase.table('episodioslista').delete().in_('episodios_idepisodio',idepisodios).execute()
            if hasattr(episodioslistas, 'error') and  episodioslistas.error:
                return JsonResponse({'error': 'Error al borrar episodio de lista de reproduccion'}, status=400)     
            episodios=supabase.table('backend_episodios').delete().in_('podcast_idpodcast',idpodcasts).execute()
            if hasattr(episodios, 'error') and  episodios.error:
                return JsonResponse({'error': 'Error al borrar episodios'}, status=400) 
            suscripcion=supabase.table('suscripcion').delete().in_('podcast_idpodcast',idpodcasts).execute()
            if hasattr(suscripcion, 'error') and suscripcion.error:
                return JsonResponse({'error': 'Error al borrar suscripcion'}, status=400)
            podcast=supabase.table('backend_podcast').delete().eq('creadores_idcreador',idCreador).execute()
            if hasattr(podcast, 'error') and podcast.error:
                return JsonResponse({'error': 'Error al borrar podcast'}, status=400)
            seguidos=supabase.table('backend_listaseguidos').delete().eq('creadores_idcreador',idCreador).execute()
            if hasattr(seguidos, 'error') and seguidos.error:
                return JsonResponse({'error': 'Error al borrar seguidos'}, status=400)
            creador=supabase.table('backend_creadores').delete().eq('idcreador',idCreador).execute()
            if hasattr(creador, 'error') and creador.error:
                return JsonResponse({'error': 'Error al borrar creador'}, status=400)
            return JsonResponse({'mensaje':'creador eliminado'})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
#########################################################################################################################
@swagger_auto_schema(
    tags=['Usuario'],
    method='post',
    operation_description="Elimina un usuario y todos sus datos relacionados (comentarios, calificaciones, listas de reproducción, etc.)",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idusuario'],
        properties={
            'idusuario': openapi.Schema(type=openapi.TYPE_STRING, description='ID del usuario a eliminar'),
        },
    ),
    responses={
        200: openapi.Response(description="Usuario eliminado exitosamente"),
        400: openapi.Response(description="Error al eliminar uno de los registros relacionados"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def borrarUsuario(request):
    if request.method=='POST':
        try:
            idusuario=request.POST.get('idusuario')
            comentarios=supabase.table('backend_comentarios').delete().eq('usuarios_idusuario',idusuario).execute()
            if hasattr(comentarios, 'error') and comentarios.error:
                return JsonResponse({'error': 'Error al borrar comentarios'}, status=400)
            calificacion=supabase.table('calificacion').delete().eq('usuarios_idusuario',idusuario).execute()
            if hasattr(calificacion, 'error') and calificacion.error:
                return JsonResponse({'error': 'Error al borrar calificacion'}, status=400)
            listasseguidos=supabase.table('backend_listaseguidos').delete().eq('usuarios_idusuario',idusuario).execute()
            if hasattr(listasseguidos, 'error') and listasseguidos.error:
                return JsonResponse({'error': 'Error al borrar listas seguidos'}, status=400)
            suscripcion=supabase.table('suscripcion').delete().eq('usuarios_idusuario',idusuario).execute()
            if hasattr(suscripcion, 'error') and suscripcion.error:
                return JsonResponse({'error': 'Error al borrar suscripcion'}, status=400)
            listasRepro=supabase.table('listareproduccion').select('idlista').eq('usuarios_idusuario',idusuario).execute()
            if hasattr(listasRepro, 'error') and listasRepro.error:
                return JsonResponse({'error': 'Error al obtener listas repro'}, status=400)
            ideplistas = [e['idlista'] for e in listasRepro.data]
            borrarEPlista=supabase.table('episodioslista').delete().in_('listareproduccion_idlista',ideplistas).execute()
            if hasattr(borrarEPlista, 'error') and borrarEPlista.error:
                return JsonResponse({'error': 'Error al borrar episodios de la lista'}, status=400)
            listas=supabase.table('listareproduccion').delete().eq('usuarios_idusuario',idusuario).execute()
            if hasattr(listas, 'error') and listas.error:
                return JsonResponse({'error': 'Error al borrar listas de reproduccion'}, status=400)
            usuario=supabase.table('backend_usuario').delete().eq('idusuario',idusuario).execute()
            if hasattr(usuario, 'error') and usuario.error:
                return JsonResponse({'error': 'Error al borrar usuario'}, status=400)
            return JsonResponse({'mensaje':'usuario eliminado'})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
 #########################################################################################################################
               
@swagger_auto_schema(
    tags=['Usuario'],
    method='post',
    operation_description="Agrega una suscripción de un usuario a un podcast y actualiza la recaudación del creador.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idusuario', 'idpodcast'],
        properties={
            'idusuario': openapi.Schema(type=openapi.TYPE_STRING, description='ID del usuario que se suscribe'),
            'idpodcast': openapi.Schema(type=openapi.TYPE_STRING, description='ID del podcast al que se suscribe'),
        },
    ),
    responses={
        200: openapi.Response(description="Suscripción exitosa"),
        400: openapi.Response(description="Error al suscribirse"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def agregarSuscripcion(request):
    if request.method=='POST':
        try:
            idUsuario=request.POST.get('idusuario')
            idPodcast=request.POST.get('idpodcast')
            data={
                "usuarios_idusuario":idUsuario,
                "podcast_idpodcast":idPodcast
            }
            suscripcion=supabase.table('suscripcion').insert(data).execute()
            if hasattr(suscripcion, 'error') and suscripcion.error:
                return JsonResponse({'error': 'Error al suscribirse'}, status=400)
            idCreador=supabase.table('backend_podcast').select('creadores_idcreador').eq('idpodcast',idPodcast).execute()
            idCreador=idCreador.data[0]['creadores_idcreador']
            recaudado=supabase.table('backend_creadores').select('recaudado').eq('idcreador',idCreador).execute()
            recaudadoActual = recaudado.data[0]['recaudado'] if recaudado.data else 0
            nuevas = recaudadoActual + 100
            actualizar = supabase.table('backend_creadores')\
                .update({'recaudado': nuevas})\
                .eq('idcreador', idCreador)\
                .execute()
            return JsonResponse({'mensaje':'Suscripcion exitosa'})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
 #########################################################################################################################
               
#actualiza un usuario segun su id, cambia los campos usuario y telefono
@swagger_auto_schema(
    tags=['Usuario'],
    method='post',
    operation_description="Actualiza el perfil del usuario, incluyendo usuario, teléfono y foto de perfil.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idusuario', 'usuario', 'telefono'],
        properties={
            'idusuario': openapi.Schema(type=openapi.TYPE_STRING, description='ID del usuario'),
            'usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de usuario'),
            'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Número de teléfono'),
            'fotoPerfil': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description='Foto de perfil (archivo)'),
        },
    ),
    responses={
        200: openapi.Response(description="Perfil actualizado"),
        400: openapi.Response(description="Datos faltantes o error al actualizar"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def actualizarUsuario(request):
    if request.method == 'POST':
        try:
            idusuario = request.POST.get('idusuario')
            usuario = request.POST.get('usuario')
            telefono = request.POST.get('telefono')
            if not idusuario or not usuario or not telefono:
                return JsonResponse({'error': 'Datos faltantes'}, status=400)
            data = {
                'usuario': usuario,
                'telefono': telefono
            }
            if 'fotoPerfil' in request.FILES:
                fotoperfil = request.FILES['fotoPerfil']
                try:
                    # Subir a Supabase Storage
                    foto_perfil_name = f'perfil_{usuario}_{uuid.uuid4().hex}.jpg'
                    supabase.storage.from_('fotosusuarios').upload(
                        path=foto_perfil_name,
                        file=fotoperfil.read(),
                    )
                    fotoperfilstr = supabase.storage.from_('fotosusuarios').get_public_url(foto_perfil_name)
                    data['fotoperfil'] = fotoperfilstr
                except Exception as e:
                    return JsonResponse({'error': f'Error al subir foto de perfil: {str(e)}'}, status=400)
             # Hacemos el update
            actualizarUsuario = supabase.table('backend_usuario').update(data).eq('idusuario', idusuario).execute()
            if hasattr(actualizarUsuario, 'error') and actualizarUsuario.error:
                return JsonResponse({'error': 'Error al actualizar perfil'}, status=400)
            return JsonResponse({'mensaje': 'Perfil actualizado'})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
#########################################################################################################################


#actualiza un creador segun su id, cambia los campos usuario,nombre, biografia,imagen de perfil, imagen donaciones y telefono
@swagger_auto_schema(
    tags=['Creador'],
    method='post',
    operation_description="Actualiza el perfil del creador, incluyendo usuario, nombre, biografía, teléfono, foto de perfil y QR de donaciones.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idcreador', 'usuario', 'nombre', 'biografia', 'telefono'],
        properties={
            'idcreador': openapi.Schema(type=openapi.TYPE_STRING, description='ID del creador'),
            'usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de usuario'),
            'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre completo'),
            'biografia': openapi.Schema(type=openapi.TYPE_STRING, description='Biografía'),
            'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Número de teléfono'),
            'fotoperfil': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description='Foto de perfil (archivo)'),
            'imgdonaciones': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description='Imagen QR para donaciones (archivo)'),
        },
    ),
    responses={
        200: openapi.Response(description="Creador actualizado"),
        400: openapi.Response(description="Datos faltantes o error al actualizar"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def actualizarCreador(request):
    if request.method=='POST':
        try:
            idcreador=request.POST.get('idcreador')
            usuario=request.POST.get('usuario')
            nombre=request.POST.get('nombre')
            biografia=request.POST.get('biografia')
            telefono=request.POST.get('telefono')
            if not idcreador or not usuario or not nombre or not biografia or not telefono:
                return JsonResponse({'error':'Datos faltantes'},status=400)
            fotoperfil = None
            if 'fotoperfil' in request.FILES:
                fotoperfil = request.FILES['fotoperfil']
                try:
                    # Subir a Supabase Storage
                    foto_perfil_name = f'perfil_{usuario}_{uuid.uuid4().hex}.jpg'
                    supabase.storage.from_('fotperfiles').upload(
                        path=foto_perfil_name,
                        file=fotoperfil.read(),
                    )
                    fotoperfil = supabase.storage.from_('fotperfiles').get_public_url(foto_perfil_name)
                except Exception as e:
                    return JsonResponse({'error': f'Error al subir foto de perfil: {str(e)}'}, status=400)
            imgdonaciones = None
            if 'imgdonaciones' in request.FILES:
                imgdonaciones = request.FILES['imgdonaciones']
                try:
                    # Subir a Supabase Storage
                    img_qr_name = f'donaciones_{usuario}_{uuid.uuid4().hex}.png'
                    supabase.storage.from_('fotoqr').upload(
                        path=img_qr_name,
                        file=imgdonaciones.read(),
                    )
                    imgdonaciones = supabase.storage.from_('fotoqr').get_public_url(img_qr_name)
                except Exception as e:
                    return JsonResponse({'error': f'Error al subir QR de donaciones: {str(e)}'}, status=400)
            data = {
                "usuario": usuario,
                "nombre": nombre,
                "biografia": biografia,
                "telefono":telefono
            }
            if fotoperfil:
                data["fotoperfil"] = fotoperfil
            if imgdonaciones:
                data["imgdonaciones"] = imgdonaciones
            actualizarCreador=supabase.table('backend_creadores').update(data).eq('idcreador',idcreador).execute()
            if hasattr(actualizarCreador,'error')and actualizarCreador.error:
                return JsonResponse({'error':'error al actualizar perfil del creador'},status=400)
            return JsonResponse({'mensaje':'Creador actualizado'})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    

#########################################################################################################################

#actualiza un podcast segun su id, cambia los campos titulo y descripcion
@swagger_auto_schema(
    tags=['Podcast'],
    method='post',
    operation_description="Actualiza el título y descripción de un podcast dado su ID.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idpodcast', 'titulo', 'descripcion'],
        properties={
            'idpodcast': openapi.Schema(type=openapi.TYPE_STRING, description='ID del podcast a actualizar'),
            'titulo': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo título del podcast'),
            'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Nueva descripción del podcast'),
        },
    ),
    responses={
        200: openapi.Response(description="Podcast actualizado"),
        400: openapi.Response(description="Datos faltantes o error al actualizar podcast"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def actualizarPodcast(request):
    if request.method=='POST':
        try:
            idPodcast=request.POST.get('idpodcast')
            titulo=request.POST.get('titulo')
            descripcion=request.POST.get('descripcion')
            if not idPodcast or not titulo or not descripcion:
                return JsonResponse({'error':'Datos faltantes'},status=400)
            data={
                'titulo':titulo,
                'descripcion':descripcion
            }
            actualizarPodcast=supabase.table('backend_podcast').update(data).eq('idpodcast',idPodcast).execute()
            if hasattr(actualizarPodcast,'error')and actualizarPodcast.error:
                return JsonResponse({'error':'Error al actualizar podcast'})
            return JsonResponse({'mensaje':'Podcast actualizado'})
        
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


#########################################################################################################################

#actualiza un episodio segun su id, cambia los campos titulo, descripcion y participantes
@swagger_auto_schema(
    tags=['Episodio'],
    method='post',
    operation_description="Actualiza los datos de un episodio dado su ID.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idepisodio', 'titulo', 'descripcion', 'participantes'],
        properties={
            'idepisodio': openapi.Schema(type=openapi.TYPE_STRING, description='ID del episodio a actualizar'),
            'titulo': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo título del episodio'),
            'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Nueva descripción del episodio'),
            'participantes': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevos participantes del episodio'),
        },
    ),
    responses={
        200: openapi.Response(description="Episodio actualizado"),
        400: openapi.Response(description="Datos faltantes o error al actualizar episodio"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def actualizarEpisodio(request):
    if request.method=='POST':
        try:
            idEpisodio=request.POST.get('idepisodio')
            titulo=request.POST.get('titulo')
            descripcion=request.POST.get('descripcion')
            participantes=request.POST.get('participantes')
            if not idEpisodio or not titulo or not descripcion or not participantes:
                return JsonResponse({'Error':'Datos faltantes'},status=400)
            data={
                'titulo':titulo,
                'descripcion':descripcion,
                'participantes':participantes
            }
            actualizarEpisodio=supabase.table('backend_episodios').update(data).eq('idepisodio',idEpisodio).execute()
            if hasattr(actualizarEpisodio,'error') and actualizarEpisodio.error:
                return JsonResponse({'Error':'Error al actualizar episodio'})
            return JsonResponse({'mensaje':'Episodio actualizado'})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

#########################################################################################################################

# views.py
import os
import uuid
import json
import wave
import subprocess
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from vosk import Model, KaldiRecognizer

# Asegúrate de que tu modelo esté en una carpeta llamada 'model'
model = Model("vosk-model/vosk-model-small-es-0.42")
FFMPEG_PATH = r"C:\ffmpeg\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"  # cambia esto a la ruta donde tengas ffmpeg.exe
import os
import uuid
import json
import requests
import subprocess
import wave
from django.http import JsonResponse
from vosk import Model, KaldiRecognizer

# Asegúrate de que el modelo esté en la carpeta correcta
model = Model("vosk-model/vosk-model-small-es-0.42")
@swagger_auto_schema(
    tags=['Transcripción'],
    method='post',
    operation_description="Transcribe el audio de una URL proporcionada (archivo .mp3). Convierte el audio a WAV mono 16kHz antes de transcribirlo.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['url'],
        properties={
            'url': openapi.Schema(type=openapi.TYPE_STRING, description='URL directa del archivo de audio en formato MP3'),
        },
    ),
    responses={
        200: openapi.Response(description="Transcripción exitosa del audio"),
        400: openapi.Response(description="URL no proporcionada o archivo inválido"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor durante la transcripción"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def transcribir_audio(request):
    if request.method == 'POST':
        try:
            audio_url = request.POST.get("url")
            if not audio_url:
                return JsonResponse({"error": "URL de audio no proporcionada"}, status=400)

            # Descargar audio
            nombre_mp3 = f"temp_{uuid.uuid4().hex}.mp3"
            with requests.get(audio_url, stream=True) as r:
                r.raise_for_status()
                with open(nombre_mp3, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            # Convertir a WAV mono 16kHz
            nombre_wav = nombre_mp3.replace(".mp3", ".wav")
            subprocess.run([
                FFMPEG_PATH, "-i", nombre_mp3,
                "-ar", "16000", "-ac", "1", nombre_wav
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            # Transcribir audio
            resultado = ""
            with wave.open(nombre_wav, "rb") as wf:
                rec = KaldiRecognizer(model, wf.getframerate())

                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        parcial = json.loads(rec.Result())
                        resultado += parcial.get("text", "") + " "

                final = json.loads(rec.FinalResult())
                resultado += final.get("text", "")

            # Eliminar archivos temporales
            os.remove(nombre_mp3)
            os.remove(nombre_wav)

            return JsonResponse({"transcripcion": resultado.strip()})

        except Exception as e:
            return JsonResponse({"error": f"Error interno: {str(e)}"}, status=500)

    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)


#########################################################################################################################
@swagger_auto_schema(
    tags=['Recuperación'],
    method='post',
    operation_description="Envía un código de recuperación por WhatsApp si el correo y rol son válidos.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['correo', 'rol'],
        properties={
            'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario o creador'),
            'rol': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Rol del solicitante (Creador o Usuario)',
                enum=['Creador', 'Usuario']
            ),
        },
    ),
    responses={
        200: openapi.Response(description="Código enviado exitosamente, se retorna el validador, ID y rol"),
        400: openapi.Response(description="Dato faltante"),
        405: openapi.Response(description="Método no permitido"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def recuperarContrasenia(request):
    if request.method=='POST':
        try:
            correo=request.POST.get('correo')
            rol=request.POST.get('rol')
            if not correo:
                return JsonResponse({'erro':'dato faltante'})
            if rol=='Creador':
                response=supabase.table('backend_creadores').select('idcreador','telefono').eq('correo',correo).execute()

                tipoid='idcreador'
                print(response.data)
            else:
                response=supabase.table('backend_usuario').select('idusuario','telefono').eq('correo',correo).execute()
                tipoid='idusuario'
                print(response.data)
            usuario=response.data[0]
            print('El usuario es')
            print(usuario)
            telefono=usuario['telefono']
            envio=enviar_codigo_whatsapp(telefono)
            codigo=envio
            return JsonResponse({'mensaje':'Codigo enviado','validador':codigo,
                             'id':usuario[tipoid],'rol':rol})
        except Exception as e:
            print(f"Error al enviar codigo: {str(e)}")
            return JsonResponse({'error': 'Error en el servidor'}, status=500)


#########################################################################################################################
@swagger_auto_schema(
    tags=['Recuperación'],
    method='post',
    operation_description="Verifica si el código ingresado coincide con el generado para recuperación de contraseña.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['codigo', 'validador', 'id', 'rol'],
        properties={
            'codigo': openapi.Schema(type=openapi.TYPE_STRING, description='Código ingresado por el usuario'),
            'validador': openapi.Schema(type=openapi.TYPE_STRING, description='Código generado previamente'),
            'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID del usuario o creador'),
            'rol': openapi.Schema(type=openapi.TYPE_STRING, description='Rol del usuario (Creador o Usuario)', enum=['Creador', 'Usuario']),
        },
    ),
    responses={
        200: openapi.Response(description="Código verificado correctamente, se retorna ID y rol del usuario"),
        401: openapi.Response(description="Código incorrecto"),
        405: openapi.Response(description="Método no permitido"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def verificar_codigo_contrasenia(request):
    if request.method == "POST":
        codigo_ingresado = request.POST.get("codigo")
        codigo_generado=request.POST.get("validador")
        id_usuario=request.POST.get('id')
        rol_usuario=request.POST.get('rol')
        print("Código ingresado:", codigo_ingresado)


        if codigo_ingresado == codigo_generado :
            

            return JsonResponse({
                'usuario': {
                    'id': id_usuario,
                    'rol': rol_usuario
                }
            })
        else:
            return HttpResponse("Código incorrecto.", status=401)

    return JsonResponse({"error": "Método no permitido"}, status=405)

#########################################################################################################################
@swagger_auto_schema(
    tags=['Recuperación'],
    method='post',
    operation_description="Cambia la contraseña de un usuario o creador.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['idusuario', 'rol', 'contraseniaNueva'],
        properties={
            'idusuario': openapi.Schema(type=openapi.TYPE_STRING, description='ID del usuario o creador'),
            'rol': openapi.Schema(type=openapi.TYPE_STRING, description='Rol del usuario (Creador o Usuario)', enum=['Creador', 'Usuario']),
            'contraseniaNueva': openapi.Schema(type=openapi.TYPE_STRING, description='Nueva contraseña del usuario'),
        },
    ),
    responses={
        200: openapi.Response(description="Contraseña cambiada correctamente"),
        400: openapi.Response(description="Datos faltantes"),
        500: openapi.Response(description="Error interno del servidor"),
        405: openapi.Response(description="Método no permitido"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def cambiarContrasenia(request):
    if request.method=='POST':
        try:
            idusuario=request.POST.get('idusuario')
            rol=request.POST.get('rol')
            if rol=='Creador':
                tabla='backend_creadores'
                tipoId='idcreador'
            else:
                tabla='backend_usuario'
                tipoId='idusuario'
            nuevacontrasenia=request.POST.get('contraseniaNueva')
            if not idusuario or not rol or not nuevacontrasenia:
                return JsonResponse({'error':'Datos faaltantes'},status=400)
            nuevaHash=make_password(nuevacontrasenia)
            cambiarContrasenia=supabase.table(tabla).update({'contrasenia':nuevaHash}).eq(tipoId,idusuario).execute()
            if hasattr(cambiarContrasenia,'error') and cambiarContrasenia.error:
                return JsonResponse({'error':' Error al cambiar la contraseña'})
            return JsonResponse({'mensaje':'Contrasenia cambiada'})
        except Exception as e:
            return JsonResponse({"error": f"Error interno: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405) 
    
#########################################################################################################################
@swagger_auto_schema(
    tags=['Usuario'],
    method='get',
    operation_description="Verifica si un usuario está suscrito a un podcast específico.",
    manual_parameters=[
        openapi.Parameter('idusuario', openapi.IN_QUERY, description="ID del usuario", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('idpodcast', openapi.IN_QUERY, description="ID del podcast", type=openapi.TYPE_STRING, required=True),
    ],
    responses={
        200: openapi.Response(description="Resultado de la verificación de suscripción (True/False)"),
        400: openapi.Response(description="Datos faltantes"),
        500: openapi.Response(description="Error interno del servidor"),
        405: openapi.Response(description="Método no permitido"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def verificarSuscripcion(request):
    if request.method=='GET':
        try:
            idUsuario=request.GET.get('idusuario')
            idPodcast=request.GET.get('idpodcast')
            if not idUsuario or not idPodcast:
                return JsonResponse({'error':'datos faltantes'})
            verificarSub=supabase.table('suscripcion').select('*').eq('usuarios_idusuario',idUsuario).eq('podcast_idpodcast',idPodcast).execute()
            if verificarSub.data:
                return JsonResponse({'suscrito':True})
            else:
                return JsonResponse({'suscrito':False})
        except Exception as e:
            return JsonResponse({"error": f"Error interno: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405) 

#########################################################################################################################
        
@swagger_auto_schema(
    tags=['Usuario'],
    method='get',
    operation_description="Verifica si un usuario (oyente) está siguiendo a un creador.",
    manual_parameters=[
        openapi.Parameter('idusuario', openapi.IN_QUERY, description="ID del usuario oyente", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('idCreador', openapi.IN_QUERY, description="ID del creador", type=openapi.TYPE_STRING, required=True),
    ],
    responses={
        200: openapi.Response(description="Resultado de la verificación de seguimiento (True/False)"),
        400: openapi.Response(description="Datos faltantes"),
        500: openapi.Response(description="Error interno del servidor"),
        405: openapi.Response(description="Método no permitido"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def verificarSeguimiento(request):
    if request.method=='GET':
        try:
            idOyente=request.GET.get('idusuario')
            idCreador=request.GET.get('idCreador')
            if not idOyente or not idCreador:
                return JsonResponse({'error':'datos faltantes'})
            verificarSeg=supabase.table('backend_listaseguidos').select('*').eq('usuarios_idusuario',idOyente)\
                .eq('creadores_idcreador',idCreador).execute()
            if verificarSeg.data:
                return JsonResponse({'siguiendo':True})
            else:
                return JsonResponse({'siguiendo':False})
        except Exception as e:
            return JsonResponse({"error": f"Error interno: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405) 


#########################################################################################################################

@swagger_auto_schema(
    tags=["Publicidad"],
    method='post',
    operation_description="Sube una nueva imagen de publicidad al almacenamiento y registra sus datos.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["fotoPublicidad", "nombrePublicidad"],
        properties={
            "fotoPublicidad": openapi.Schema(
                type=openapi.TYPE_STRING,  # IMPORTANTE: no uses TYPE_FILE aquí, sino TYPE_STRING
                format="binary",           # formato para archivos (multipart/form-data)
                description="Imagen de la publicidad"
            ),
            "nombrePublicidad": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Nombre asignado a la publicidad"
            ),
        },
    ),
    responses={
        200: openapi.Response(description="Publicidad subida con éxito"),
        400: openapi.Response(description="Error al subir foto de perfil"),
        405: openapi.Response(description="Método no permitido"),
    },
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def subirPublicidad(request):
    if request.method=='POST':
        fotopublicidad= None
        if 'fotoPublicidad' in request.FILES:
            nombrePublicidad=request.POST.get('nombrePublicidad')
            fotopublicidad = request.FILES['fotoPublicidad']
            try:
                # Subir a Supabase Storage
                foto_publicidad_name = f'perfil_{nombrePublicidad}_{uuid.uuid4().hex}.jpg'
                supabase.storage.from_('publicidad').upload(
                        path=foto_publicidad_name,
                        file=fotopublicidad.read(),
                )
                fotopublicidad = supabase.storage.from_('publicidad').get_public_url(foto_publicidad_name)
                data={
                    'imagen':fotopublicidad,
                    'nombrePublicidad':nombrePublicidad
                }
                registro=supabase.table('publicidad').insert(data).execute()
                return JsonResponse({'mensaje':'publicidad subida'})
            except Exception as e:
                print(request.POST)
                print(request.FILES)
                print("ERROR SUPABASE:", str(e))
                return JsonResponse({'error': f'Error al subir foto de perfil: {str(e)}'}, status=400)


#########################################################################################################################

import random
from django.http import JsonResponse
@swagger_auto_schema(
    tags=["Publicidad"],
    method='get',
    operation_description="Obtiene dos publicidades aleatorias de la base de datos.",
    responses={
        200: openapi.Response(
            description="Lista de publicidades",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "publicidades": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "idpublicidad": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "imagen": openapi.Schema(type=openapi.TYPE_STRING, description="URL de la imagen"),
                                "nombrePublicidad": openapi.Schema(type=openapi.TYPE_STRING),
                                # incluye otras propiedades según tu tabla
                            },
                        ),
                    ),
                },
            ),
        ),
        400: openapi.Response(description="Error en la solicitud"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}],
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def obtenerPublicidad(request):
    if request.method == 'GET':
        try:
            response = supabase.table('publicidad').select('idpublicidad').execute()
            # Para debug, imprime el objeto response y sus atributos
            print("Response:", response)
            print("Response error:", getattr(response, 'error', None))
            print("Response data:", getattr(response, 'data', None))
            if getattr(response, 'error', None) is not None:
                return JsonResponse({'error': 'Error al obtener IDs de publicidad'}, status=400)
            ids = [item['idpublicidad'] for item in response.data]
            if len(ids) < 2:
                return JsonResponse({'error': 'No hay suficientes publicidades'}, status=400)
            random_ids = random.sample(ids, 2)
            response2 = supabase.table('publicidad').select('*').in_('idpublicidad', random_ids).execute()
            if getattr(response2, 'error', None) is not None:
                return JsonResponse({'error': 'Error al obtener publicidades'}, status=400)

            return JsonResponse({'publicidades': response2.data})

        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
#########################################################################################################################

from datetime import timedelta

@swagger_auto_schema(
    tags=["Notificaciones"],
    method='get',
    operation_description="Obtiene los episodios publicados en las últimas 24 horas por los creadores que el usuario sigue.",
    manual_parameters=[
        openapi.Parameter(
            'idusuario',
            openapi.IN_QUERY,
            description="ID del usuario que consulta las notificaciones",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Lista de episodios recientes de los creadores seguidos",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "notificaciones": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id_episodio": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "titulo": openapi.Schema(type=openapi.TYPE_STRING),
                                "fechapublicacion": openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                                # Agrega más campos si tu tabla tiene otros datos
                            }
                        )
                    )
                }
            )
        ),
        400: openapi.Response(description="Error al obtener notificaciones"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def episodioNotificaciones(request):
    if request.method=='GET':
        try:
            idusuario=request.GET.get('idusuario')
            siguiendo=supabase.table('backend_listaseguidos').select('creadores_idcreador').eq('usuarios_idusuario',idusuario).execute()
            idsSiguiendo = [e['creadores_idcreador'] for e in siguiendo.data]
            podcasts=supabase.table('backend_podcast').select('idpodcast').in_('creadores_idcreador',idsSiguiendo).execute()
            idsPodcast = [e['idpodcast'] for e in podcasts.data]
            hace_24_horas = datetime.datetime.utcnow() - timedelta(hours=24)
            fecha_corte = hace_24_horas.isoformat()
            episodiosNotificacion=supabase.table('backend_episodios').select('*','podcast_idpodcast(titulo,creadores_idcreador(nombre))').in_('podcast_idpodcast',idsPodcast)\
                .gte('fechapublicacion', fecha_corte) \
                .execute()
            if hasattr( episodiosNotificacion,'error')and episodiosNotificacion.error:
                print("Error:", episodiosNotificacion.error)
                return JsonResponse({'error':'error al obtener notificaciones'})
            else:
                registros = episodiosNotificacion.data
                return JsonResponse({'notificaciones':registros})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)


#########################################################################################################################
@swagger_auto_schema(
    method='get',
    tags=["Recomendaciones"],
    operation_description=(
        "Obtiene el episodio más visto en las últimas 24 horas. "
        "Si no hay episodios recientes, retorna el episodio con más visualizaciones en general."
    ),
    responses={
        200: openapi.Response(
            description="Episodio más visto del día o en general",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "episodio": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id_episodio": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "titulo": openapi.Schema(type=openapi.TYPE_STRING),
                            "visualizaciones": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "fechapublicacion": openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                            "podcast_idpodcast": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "titulo": openapi.Schema(type=openapi.TYPE_STRING),
                                    "creadores_idcreador": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "idcreador": openapi.Schema(type=openapi.TYPE_INTEGER),
                                            "nombre": openapi.Schema(type=openapi.TYPE_STRING),
                                        }
                                    )
                                }
                            )
                        }
                    )
                }
            )
        ),
        400: openapi.Response(description="Error al obtener episodio del día"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def episodioDia(request):
    if request.method=='GET':
        try:
            hace_24_horas = datetime.datetime.utcnow() - timedelta(hours=24)
            fecha_corte = hace_24_horas.isoformat()
            episodioDia=supabase.table('backend_episodios').select('*','podcast_idpodcast(titulo, creadores_idcreador(idcreador,nombre))').gte('fechapublicacion', fecha_corte)\
            .order('visualizaciones', desc=True)\
            .limit(1)\
            .execute()
            if not episodioDia.data:
                episodioDia=supabase.table('backend_episodios').select('*','podcast_idpodcast(titulo, creadores_idcreador(idcreador,nombre))')\
            .order('visualizaciones', desc=True)\
            .limit(1)\
            .execute()
            if hasattr(episodioDia,'error')and episodioDia.error:
                return JsonResponse({'error':'Error al obtener episodio del dia'})
            return JsonResponse({'episodio':episodioDia.data[0]})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
#########################################################################################################################

@swagger_auto_schema(
    method='get',
    tags=["Podcast"],
    operation_description="Obtiene todos los episodios relacionados a un podcast específico usando su ID.",
    manual_parameters=[
        openapi.Parameter(
            'idpodcast', openapi.IN_QUERY, description="ID del podcast",
            type=openapi.TYPE_STRING, required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Lista de episodios del podcast",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "episodios": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id_episodio": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "titulo": openapi.Schema(type=openapi.TYPE_STRING),
                                "descripcion": openapi.Schema(type=openapi.TYPE_STRING),
                                "fechapublicacion": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
                                "visualizaciones": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "podcast_idpodcast": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "titulo": openapi.Schema(type=openapi.TYPE_STRING),
                                        "creadores_idcreador": openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                "idcreador": openapi.Schema(type=openapi.TYPE_INTEGER),
                                                "nombre": openapi.Schema(type=openapi.TYPE_STRING),
                                            }
                                        )
                                    }
                                )
                            }
                        )
                    )
                }
            )
        ),
        400: openapi.Response(description="Error al obtener episodios del podcast"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def episodios_podcast(request):
    if request.method=='GET':
        try:
            idpodcast=request.GET.get('idpodcast')
            episodios=supabase.table('backend_episodios').select('*','podcast_idpodcast(titulo, creadores_idcreador(idcreador,nombre))').eq('podcast_idpodcast',idpodcast).execute()
            if hasattr(episodios,'error') and episodios.error:
                return JsonResponse({'error':'error al obtener episodios del podcast'})
            return JsonResponse({'episodios':episodios.data})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
#########################################################################################################################
@swagger_auto_schema(
    method='get',
    tags=["Podcast"],
    operation_description="Verifica si un podcast específico es premium mediante su ID.",
    manual_parameters=[
        openapi.Parameter(
            'idpodcast', openapi.IN_QUERY,
            description="ID del podcast a verificar",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Información de premium del podcast",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "premium": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "idpodcast": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "nombre": openapi.Schema(type=openapi.TYPE_STRING),
                                "premium": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                # Puedes añadir más campos si tu tabla los tiene
                            }
                        )
                    )
                }
            )
        ),
        400: openapi.Response(description="Error al verificar premium"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def verificarPremium(request):
    if request.method=='GET':
        try:
            idpodcast=request.GET.get('idpodcast')
            response=supabase.table('backend_podcast').select('*').eq('idpodcast',idpodcast).execute()
            if hasattr(response,'error') and response.error:
                return JsonResponse({'error':'error al verificar premium'})
            return JsonResponse({'premium':response.data})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
        

#########################################################################################################################

@swagger_auto_schema(
    method='get',
    tags=["Podcast"],
    operation_description="Lista todos los podcasts junto con el nombre del creador.",
    responses={
        200: openapi.Response(
            description="Lista de podcasts",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "podcasts": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "idpodcast": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "nombre": openapi.Schema(type=openapi.TYPE_STRING),
                                "descripcion": openapi.Schema(type=openapi.TYPE_STRING),
                                "premium": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                "creadores_idcreador": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "nombre": openapi.Schema(type=openapi.TYPE_STRING)
                                    }
                                )
                                # Puedes agregar más campos si es necesario
                            }
                        )
                    )
                }
            )
        ),
        400: openapi.Response(description="Error al obtener podcast admin"),
        500: openapi.Response(description="Error interno del servidor"),
    },
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def listarPodcasts(request):
    if request.method=='GET':
        try:
            podcasts=supabase.table('backend_podcast').select('*','creadores_idcreador(nombre)').execute()

            if hasattr(podcasts,'error') and podcasts.error:
                return JsonResponse({'error':'error al obtener podcast admin'})
            return JsonResponse({'podcasts':podcasts.data})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

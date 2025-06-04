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

@csrf_exempt
def login_usuario(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        usuario = request.POST.get('usuario')
        contrasenia = request.POST.get('contrasenia')
        rol = request.POST.get('rol')
        
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
        print(f"Error en login: {str(e)}")
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


# Configuración de Supabase (ajusta con tus claves reales)

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

            return JsonResponse({
                'exito': 'vistas aumentadas en 1'
            })
        except Exception as e:
            return JsonResponse({'error': 'error al actualizar visualizaciones'}, status=500)
            

from django.http import JsonResponse
from django.utils import timezone
import traceback
import os
import uuid


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


#para el dashBoard de creador
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




##endpoints nuevos
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
                
#actualiza un usuario segun su id, cambia los campos usuario y telefono
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

#actualiza un creador segun su id, cambia los campos usuario,nombre, biografia,imagen de perfil, imagen donaciones y telefono
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
#actualiza un podcast segun su id, cambia los campos titulo y descripcion
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

#actualiza un episodio segun su id, cambia los campos titulo, descripcion y participantes
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

import random
from django.http import JsonResponse
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

            import random
            random_ids = random.sample(ids, 2)

            response2 = supabase.table('publicidad').select('*').in_('idpublicidad', random_ids).execute()

            if getattr(response2, 'error', None) is not None:
                return JsonResponse({'error': 'Error al obtener publicidades'}, status=400)

            return JsonResponse({'publicidades': response2.data})

        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
        
from datetime import timedelta
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
        


def listarPodcasts(request):
    if request.method=='GET':
        try:
            podcasts=supabase.table('backend_podcast').select('*','creadores_idcreador(nombre)').execute()

            if hasattr(podcasts,'error') and podcasts.error:
                return JsonResponse({'error':'error al obtener podcast admin'})
            return JsonResponse({'podcasts':podcasts.data})
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

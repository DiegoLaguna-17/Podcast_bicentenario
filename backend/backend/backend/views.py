# backend/views.py
from django.http import JsonResponse
from .db_connection import obtener_conexion
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models.Usuarios import Usuario
# backend/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Creadores
from django.utils.crypto import get_random_string
from django.views import View
import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import os







from django.shortcuts import render
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

from datetime import datetime


import logging
from django.utils import timezone 


logger = logging.getLogger(__name__)

from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def episodios(request):
    if request.method=='GET':
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    
                    
SELECT bc.idepisodio,bc.titulo,bc.descripcion,bc.fechapublicacion,bc.audio,bc.participantes, c.nombre as creador, p.titulo as podcast
                    FROM backend_episodios bc, 
                    backend_creadores c,
                    backend_podcast p
                    WHERE bc.podcast_idpodcast  = p.idpodcast
                    AND p.creadores_idcreador =c.idcreador
                    AND bc.visible=True
                    ORDER BY fechapublicacion DESC
                    LIMIT 10;         
                    """
                )
                columns= [col[0] for col in cursor.description] 
                episodios = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
                return JsonResponse({'episodios': episodios}, status=200)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
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



@csrf_exempt
def perfil_usuario(request):
    if request.method=='POST':
        try:
            
            id=request.POST.get('id')
            rol=request.POST.get('rol')
            if rol in ['Administrador','Oyente']:
                response=response = supabase.table('backend_usuario').select('*').eq('idusuario', id).execute()
            else:
                response=response = supabase.table('backend_creadores').select('*').eq('idcreador', id).execute()
            
            if not response.data:
                return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
            
            usuario_data=response.data[0]
            
            if rol in ['Administrador','Oyente']:
                usuario={
                    'id':usuario_data['idusuario'],
                    'usuario':usuario_data['usuario'],
                    'rol':usuario_data['rol'],
                    'correo':usuario_data['correo'],
                    'fecha':usuario_data['fecha_ingreso']
                }
            else:
                usuario={
                    'id':usuario_data['idcreador'],
                    'usuario':usuario_data['usuario'],
                    'nombre':usuario_data['nombre'],
                    'correo':usuario_data['correo'],
                    'rol':'Creador',
                    'fotoPerfil':usuario_data['fotoperfil'],
                    'biografia':usuario_data['biografia'],
                    'donaciones':usuario_data['imgdonaciones']
                }
            
            return JsonResponse(usuario)
        except Exception as e:
        # Loggear el error para debugging
            print(f"Error en login: {str(e)}")
            return JsonResponse({'error': 'Error en el servidor'}, status=500)


        



@csrf_exempt
def login_usuario(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        # Obtener datos del formulario
        usuario = request.POST.get('usuario')
        contrasenia = request.POST.get('contrasenia')
        rol = request.POST.get('rol')
        
        # Validar campos obligatorios
        if not all([usuario, contrasenia, rol]):
            return JsonResponse({'error': 'Usuario, contraseña y rol son requeridos'}, status=400)
        
        # Determinar la tabla según el rol
        if rol == 'Creador':
            user='idcreador'
            tabla = 'backend_creadores'
        elif rol in ['Administrador', 'Oyente']:
            tabla = 'backend_usuario'
            user='idusuario'
        else:
            return JsonResponse({'error': 'Rol no válido'}, status=400)
        
        # Buscar usuario en la base de datos
        response = supabase.table(tabla).select('*').eq('correo', usuario).execute()
        
        if not response.data:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        
        usuario_data = response.data[0]
        
        # Verificar contraseña (asumiendo que hay un campo 'contrasenia' en la BD)
        if check_password(usuario_data.get('contrasenia'),contrasenia):
            return JsonResponse({'error': 'Contraseña incorrecta'}, status=401)
        
        # Verificar rol si está almacenado en la tabla
        if 'rol' in usuario_data and usuario_data['rol'] != rol:
            return JsonResponse({'error': 'El rol no coincide para este usuario'}, status=403)
        if 'rol' in usuario_data and usuario_data['rol'] in ['Administrador', 'Oyente']:
            usuario={
                'id':usuario_data['idusuario'],
                'rol':usuario_data['rol']
            }
            
        else:
            usuario={
                'id':usuario_data['idcreador'],
                'rol':'Creador'
                
            }
        
        # Login exitoso
        return JsonResponse(usuario)
        
    except Exception as e:
        # Loggear el error para debugging
        print(f"Error en login: {str(e)}")
        return JsonResponse({'error': 'Error en el servidor'}, status=500)



def mostrar_formulario_episodio(request):
    return render(request, 'episodio.html')

@csrf_exempt
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

            # Convertir y validar fecha
            try:
                fecha_hora = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M")
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






@csrf_exempt
def podcasts_por_creador(request):
    if request.method == 'POST':
        try:
            id_creador = request.POST.get('id')
            response = supabase.table('backend_podcast')\
                               .select('*')\
                               .eq('creadores_idcreador', id_creador)\
                               .execute()
            podcasts = response.data or []

            return JsonResponse({'podcasts': podcasts}, status=200)

        except Exception as e:
            print(f"Error en obtener podcasts: {str(e)}")
            return JsonResponse({'error': 'Error en el servidor'}, status=500)



def mostrar_formulario_podcast(request):
    return render(request, 'podcast.html')




@csrf_exempt
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






@csrf_exempt
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

@csrf_exempt
def seguirCreador(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Verificar que los campos requeridos estén presentes
            if 'usuarios_idusuario' not in data or 'creadores_idcreador' not in data:
                return JsonResponse({'error': 'Faltan campos requeridos'}, status=400)
            
            # Insertar directamente (ya que managed=False)
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO backend_listaseguidos 
                    (usuarios_idusuario, creadores_idcreador)
                    VALUES (%s, %s)
                    RETURNING creadores_idcreador
                    """,
                    [data['usuarios_idusuario'], data['creadores_idcreador']]
                )
                new_id = cursor.fetchone()[0]
                # Corregido el typo en 'readores_idcreador' a 'creadores_idcreador'
                return JsonResponse({
                    'usuarios_idusuario': data['usuarios_idusuario'], 
                    'creadores_idcreador': data['creadores_idcreador']
                }, status=201)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


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



def mostrar_formulario_registro(request):
    return render(request, 'registro.html')

@csrf_exempt
def registro(request):
    if request.method == 'POST':
        try:
            # 1. Obtener datos del formulario
            usuario = request.POST.get('usuario')
            contrasenia = request.POST.get('contrasenia')
            nombre = request.POST.get('nombre')
            correo = request.POST.get('correo')
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
            }
            
            response = supabase.table('backend_creadores').insert(data).execute()

            # 5. Verificar si hubo errores
            if hasattr(response, 'error') and response.error:
                return JsonResponse({'error': 'Error al registrar en Supabase'}, status=400)

            # 6. Éxito: Redirigir o devolver éxito
            return render(request, 'registro_exitoso.html', {"message": "¡Registro exitoso!"})
        except Exception as e:
            # Captura cualquier error inesperado y devuelve un mensaje genérico
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

    # Si no es POST, mostrar el formulario
    return render(request, 'registro.html')


def mostrar_formulario_oyente(request):
    return render(request, 'usuario.html')



@csrf_exempt
def crear_usuario(request):
    if request.method == 'POST':
        try:
            usuario=request.POST.get('usuario')
            contrasenia=request.POST.get('contrasenia')
            rol='Oyente'
            correo=request.POST.get('correo')
            fecha=timezone.now().date().isoformat()
            contrasenia_hash=make_password(contrasenia)
            data = {
                "usuario":usuario,
                "contrasenia":contrasenia_hash,
                "rol":rol,
                "correo":correo,
                "fecha_ingreso":fecha,
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


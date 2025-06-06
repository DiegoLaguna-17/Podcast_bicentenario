"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Documentacion POdcast Bicentenario",
      default_version='v1',
      description="Documentación API con Swagger usando drf-yasg",
      terms_of_service="https://www.tusitio.com/terms/",
      contact=openapi.Contact(email="contacto@tusitio.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

#endpoints de inicio
    
    path('login/',views.login_usuario,name='login'),
    path('verificarCodigo/',views.verificar_codigo,name='verficar_mensaje'),
    #endpoints de registro
    path('registro/usuario/', views.registro_usuario, name='crear_usuario'),##con Postman
    path('registro/creador/', views.registro_creador, name='registro'),
    #cargar el perfil
    path('perfil/',views.perfil_usuario,name='perfil'),

    #enpoints oyente
    path('usuarios/seguirCreador/',views.seguirCreador,name='seguir_creador'),##con Postman
    path('usuarios/dejarSeguir/',views.dejarSeguirCreador,name='dejar_seguir'),
    path('usuarios/actualizarUsuario/',views.actualizarUsuario,name="actualizar_usuario"),
    #path('creadores/mostrar/', views.mostrar_creadores, name='mostrar_creadores'),
    path('usuarios/subirCalificacion/',views.crear_calificacion,name='subir-Calificacion'),
    #
    path('usuarios/crearLista/',views.crearListaReproduccion,name='crear_lista'),
    path('usuarios/agregarEpisodioLista/',views.agregarEpisodioLista,name='agregar_apisodio'),
    path('usuarios/quitarEpisodioLista/',views.quitarEpisodio,name='quitar_ep_lista'),

    path('usuarios/donar/',views.donarCreador,name="donar_creador"),
    path('usuarios/obtenerSeguimientos/', views.obtenerSeguimientos, name='obtener_seguimientos'),##lista que sigue el usuario
    path('usuarios/suscribirse/',views.agregarSuscripcion,name="agregar_suscripcion"),
    path('usuarios/comentar/', views.subir_comentarios,name='subir_comentario'),
    path('usuarios/notificaciones/',views.episodioNotificaciones,name="episodios_notificacion"),
    path('usuarios/episodioDia/',views.episodioDia,name="episodio_dia"),

    path('usuarios/recuperarContrasenia/',views.recuperarContrasenia,name="recuperar_contrasenia"),
    path('usuarios/verificarCodigoContrasenia/',views.verificar_codigo_contrasenia,name="codigo_contrasenia"),
    path('usuarios/cambiarContrasenia/',views.cambiarContrasenia,name="cambiar_contrasenia"),
    path('usuarios/verificarSuscripcion/',views.verificarSuscripcion,name="verificar_suscripcion"),
    path('usuarios/verificarSeguimiento/',views.verificarSeguimiento,name="verificar_seguimiento"),
    path('podcast/episodios/',views.episodios_podcast,name="episodios podcast"),
    path('episodios/verificarPremium/',views.verificarPremium,name="verificar_premium"),
    #crear lista de reproduccion
    
    ##ENDPOINTS PARA CREADOR
    path('creador/',views.perfil_creador,name='creador'),
    path('creador/podcasts/', views.podcasts_por_creador, name='podcasts-creador'),
    path('podcast/',views.crear_podcast,name='podcast'),
    path('episodio/',views.subir_episodio,name='subir_episodio'),
    path('actualizarCreador/',views.actualizarCreador,name="actualizar_creador"),
    path('actualizarPodcast/',views.actualizarPodcast,name="actualizar_podcast"),
    path('actualizarEpisodio/',views.actualizarEpisodio,name="actualizar_episodio"),

    #endpoint de dashboard creador
    path('obtenerVistasCreador/',views.obtener_visualizaciones,name='vistas_creador'),
    path('obtenerMasVisto/',views.obtener_ep_mas_visto,name='episodio_mas_visto'),
    path('obtenerConteoSeguidores/',views.obtenerSeguidores,name='obtener_seguidores'),

    
#PARA TI
    path('episodios/',views.episodios,name='episodios_para_ti'),

    
#BUSCAR
    path('buscar_general/', views.buscar_general, name='buscar_general'),
    path('buscar_anio/',views.buscar_anio,name='buscar_anio'),
    path('buscar_tematica/', views.buscar_tematica,name='buscar_tematica'),
#REPRODUCTOR
    path('actualizar_visualizaciones/',views.sumar_visualizacion,name='actualizar_visualizaciones'),
    path('obtenerCalificaciones/',views.obtener_calificacion,name='obtener_calificaciones'),
    path('obtener_comentarios/',views.obtenerComentarios,name='obtener_comentarios'),
    path('transcribir/',views.transcribir_audio,name="transcribir_audio"),

    
   
    #enpoints administrador
    path('borrarUsuario/',views.borrarUsuario,name="borrar_usuario"),
    path('borrarCreador/',views.borrarCreador,name='borrar_creador'),
    path('borrarPodcast/',views.borrarPodcast,name="borrar_podcast"),
    path('borrarEpisodio/',views.borrarEpisodio,name="borrar_episodio"),
    path('borrarComentario/',views.borrarComentario,name='borrar_comentario'),
    path('usuarios/listar/', views.listar_usuarios, name='listar_usuarios'),##con Postman
    path('creadores/listar/',views.listar_creadores,name='listar_creadores'),
    path('subirPublicidad/',views.subirPublicidad,name="subir_publicidad"),
    path('obtenerPublicidad/',views.obtenerPublicidad,name="obtener_publicidad"),
    path('listarPodcasts/',views.listarPodcasts,name="listar_podcasts"),
 

 #documentacion swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
 
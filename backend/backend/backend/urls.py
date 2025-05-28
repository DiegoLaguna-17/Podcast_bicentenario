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
from django.urls import path


from django.urls import path
from . import views

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
    #path('creadores/mostrar/', views.mostrar_creadores, name='mostrar_creadores'),
    path('subirCalificacion/',views.crear_calificacion,name='subir-Calificacion'),
    path('usuarios/crearLista/',views.crearListaReproduccion,name='crear_lista'),
    path('usuarios/agregarEpisodioLista/',views.agregarEpisodioLista,name='agregar_apisodio'),
    path('usuarios/quitarEpisodioLista/',views.quitarEpisodio,name='quitar_ep_lista'),
    path('usuarios/donar/',views.donarCreador,name="donar_creador"),
    path('usuarios/obtenerSeguimientos/', views.obtenerSeguimientos, name='obtener_seguimientos'),##lista que sigue el usuario
    path('usuarios/suscribirse/',views.agregarSuscripcion,name="agregar_suscripcion"),
    path('comentar/', views.subir_comentarios,name='subir_comentario'),
    #crear lista de reproduccion
    
    ##ENDPOINTS PARA CREADOR
    path('creador/',views.perfil_creador,name='creador'),
    path('creador/podcasts/', views.podcasts_por_creador, name='podcasts-creador'),
    path('podcast/',views.crear_podcast,name='podcast'),
    path('episodio/',views.subir_episodio,name='subir_episodio'),
    #endpoint de dashboard creador
    path('obtenerVistasCreador/',views.obtener_visualizaciones,name='vistas_creador'),
    path('obtenerMasVisto/',views.obtener_ep_mas_visto,name='episodio_mas_visto'),
    path('obtenerConteoSeguidores/',views.obtenerSeguidores,name='obtener_seguidores'),
    
    
    
    
    
    
#PARA TI
    path('episodios/',views.episodios,name='episodios_para_ti'),

    
#BUCAR
    path('buscar_general/', views.buscar_general, name='buscar_general'),
    path('buscar_anio/',views.buscar_anio,name='buscar_anio'),
    path('buscar_tematica/', views.buscar_tematica,name='buscar_tematica'),
#REPRODUCTOR
    path('actualizar_visualizaciones/',views.sumar_visualizacion,name='actualizar_visualizaciones'),
    path('obtenerCalificaciones/',views.obtener_calificacion,name='obtener_calificaciones'),
    path('obtener_comentarios/',views.obtenerComentarios,name='obtener_comentarios'),

    
   
    #enpoints administrador
    path('borrarUsuario/',views.borrarUsuario,name="borrar_usuario"),
    path('borrarCreador/',views.borrarCreador,name='borrar_creador'),
    path('borrarPodcast/',views.borrarPodcast,name="borrar_podcast"),
    path('borrarEpisodio/',views.borrarEpisodio,name="borrar_episodio"),
    path('borrarComentario/',views.borrarComentario,name='borrar_comentario'),
    path('usuarios/listar/', views.listar_usuarios, name='listar_usuarios'),##con Postman
    path('creadores/listar/',views.listar_creadores,name='listar_creadores'),
    







]
 
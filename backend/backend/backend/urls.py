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
    path('registro/usuario/', views.registro_usuario, name='crear_usuario'),##con Postman
    path('usuarios/listar/', views.listar_usuarios, name='listar_usuarios'),##con Postman
    path('creadores/listar/',views.listar_creadores,name='listar_creadores'),
        path('creadores/registrar/', views.mostrar_formulario_registro, name='registrar'),
    path('registro/creador/', views.registro_creador, name='registro'),
    path('creadores/mostrar/', views.mostrar_creadores, name='mostrar_creadores'),
    path('usuarios/seguirCreador/',views.seguirCreador,name='seguir_creador'),##con Postman
    path('usuarios/obtenerSeguimientos/', views.obtenerSeguimientos, name='obtener_seguimientos'),##con Postman
    path('podcast/',views.crear_podcast,name='podcast'),
    path('creadores/crearPodcast/',views.mostrar_formulario_podcast,name='vistapodcast'),
    path('creador/podcasts/', views.podcasts_por_creador, name='podcasts-creador'),

    path('creador/subirEpisodio/',views.mostrar_formulario_episodio,name='vistaepisodio'),
    path('episodio/',views.subir_episodio,name='subir_episodio'),
    path('login/',views.login_usuario,name='login'),
    path('crear/oyente/',views.mostrar_formulario_oyente,name='crearOyente'),
    path('perfil/',views.perfil_usuario,name='perfil'),
    path('creador/',views.perfil_creador,name='creador'),

    path('episodios/',views.episodios,name='creador'),
    path('comentar/', views.subir_comentarios,name='subir_comentario'),
    path('obtener_comentarios/',views.obtenerComentarios,name='obtener_comentarios'),
    path('buscar_general/', views.buscar_general, name='buscar_general'),
    path('buscar_anio/',views.buscar_anio,name='buscar_anio'),
    path('buscar_tematica/', views.buscar_tematica,name='buscar_tematica'),
    path('actualizar_visualizaciones/',views.sumar_visualizacion,name='actualizar_visualizaciones'),
    path('verificarCodigo/',views.verificar_codigo,name='verficar_mensaje'),
    path('subirCalificacion/',views.crear_calificacion,name='subir-Calificacion'),
    path('obtenerCalificaciones/',views.obtener_calificacion,name='obtener_calificaciones'),
    #endpoint de dashboard creador
    path('obtenerVistasCreador/',views.obtener_visualizaciones,name='vistas_creador'),
    path('obtenerMasVisto/',views.obtener_ep_mas_visto,name='episodio_mas_visto'),
    path('obtenerConteoSeguidores/',views.obtenerSeguidores,name='obtener_seguidores')




]
 
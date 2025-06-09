import { Route,ActivatedRoute } from '@angular/router';
import { Component,Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import { NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-gestion-episodios',
  imports: [CommonModule,FormsModule],
  templateUrl: './gestion-episodios.component.html',
  styleUrl: './gestion-episodios.component.css'
})
export class GestionEpisodiosComponent {
  idpodcast:any
  episodios:any[]=[]
  errorRespuesta:any
  cargando:boolean=false
  mostrarModal:boolean=false
  idEditar:any
  tituloPodcast:string=''
  tituloEditar:string=''
  descripcionEditar:string=''
  participantesEditar:string=''
  imagen:any
  imagenSeleccionada:any
  modalComentarios:boolean=false;
  comentarios:any[]=[]
  headers:any
  constructor(private route: ActivatedRoute,private http: HttpClient,) {
    const token = localStorage.getItem('access_token');
  
    if (!token) {
      this.errorRespuesta = 'No se encontró token de autenticación.';
      return;
    }
    this.headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
    });
  this.route.queryParams.subscribe(params => {
    this.idpodcast=params['id'];
    this.tituloPodcast=params['titulo'];
  });
  this.cargarEpisodios()
}

cargarEpisodios(){
  this.cargando=true;
  const headers=this.headers
  const enpoint= environment.apiUrl+'/podcast/episodios/?idpodcast='+this.idpodcast;
  this.http.get<{episodios:any}>(enpoint,{headers}).subscribe({
    next:(response)=>{
      console.log(response.episodios)
      this.episodios=response.episodios
      this.cargando=false;
    },
    error:(error)=>{
      console.error('Error en gestion de usuarios:', error);
      this.errorRespuesta = 'Error al cargar el perfil.';
    }
  });

}
gestionComentarios(episodio:any){
  this.modalComentarios=true;
  this.cargarComentarios(episodio)
}
cargarComentarios(episodio:any){
  const headers=this.headers
  const endpoint=environment.apiUrl+'/obtener_comentarios/?episodios_idepisodio='+episodio.idepisodio;
  this.http.get<{comentarios:any}>(endpoint,{headers}).subscribe({
    next:(response)=>{
      this.comentarios=response.comentarios
    },
    error:(error)=>{
      console.error('Error en gestion de comentarios:', error);
      this.errorRespuesta = 'Error al cargar los comentarios.';
    }
  });

}

cerrarModalComentario(){
  this.modalComentarios=false;
  this.idEditar='';
    this.tituloEditar='';
    this.descripcionEditar='';
    this.participantesEditar='';
}
eliminarComentario(comentario:any){
  const headers=this.headers
    const confirmar=window.confirm('Desea eliminar permanentemente el comentario?')
    if(confirmar){
      const endpoint=environment.apiUrl+'/borrarComentario/';
      const eliminar=new FormData()
      eliminar.append('idcomentario',comentario.idcomentario)
      this.http.post(endpoint,eliminar,{headers}).subscribe({
        next:(response)=>{
          alert('Comentario eliminado')
          this.cerrarModalComentario()
        },
        error:(error)=>{
          console.error('Error al eliminar comentario:', error);
          this.errorRespuesta = 'Error al eliminar comentario.';
        }
      });
    }else{
      this.cerrarModalComentario()
    }
}

  editar(episodio:any){
    this.mostrarModal=true;
    this.idEditar=episodio.idepisodio;
    this.tituloEditar=episodio.titulo;
    this.descripcionEditar=episodio.descripcion;
    this.participantesEditar=episodio.participantes;

  }
  cerrarModal(){
    this.mostrarModal=false;
    this.idEditar='';
    this.tituloEditar='';
    this.descripcionEditar='';
    this.participantesEditar='';

  }
  

actualizarEpisodio(){
  const headers=this.headers
  const confirmar=window.confirm('Actualizar el episodio '+this.tituloEditar+'?' );
  if(confirmar){
    const endpoint=environment.apiUrl+'/actualizarEpisodio/';
    const actualizar=new FormData()
    actualizar.append('idepisodio',this.idEditar);
    actualizar.append('titulo',this.tituloEditar);
    actualizar.append('descripcion',this.descripcionEditar);
    actualizar.append('participantes',this.participantesEditar);
    this.http.post(endpoint,actualizar,{headers}).subscribe({
      next:(response)=>{
        alert('Episodio actualizado')
        this.cerrarModal();
        this.cargarEpisodios();
      },
      error:(error)=>{
        console.error('Error al actualizar episodio:', error);
        this.errorRespuesta = 'Error al actualizar episodio.';
      }
    });

  }else{
    this.cerrarModal();
  }
}

eliminarEpisodio(episodio:any){
  const confirmar=window.confirm('Desea eliminar permanentemente el episodio '+episodio.titulo+'?')
  if(confirmar){
    const confirmar2=window.confirm('La siguiente accion no podra deshacerse. ¿Eliminar permanentemente  '+episodio.tituloEditar+'?');
    if(confirmar2){
      const headers=this.headers
      const enpoint=environment.apiUrl+'/borrarEpisodio/'
      const eliminar=new FormData()
      eliminar.append('idepisodio',episodio.idepisodio)
      this.http.post(enpoint,eliminar,{headers}).subscribe({
        next:(response)=>{
          alert('Episodio eliminado permanentemente')
          this.cargarEpisodios()
        },
        error:(error)=>{
          console.error('Error al eliminar episodio:', error);
          this.errorRespuesta = 'Error al eliminar episodio..';
        }
      });
    }
  }
}

  
}

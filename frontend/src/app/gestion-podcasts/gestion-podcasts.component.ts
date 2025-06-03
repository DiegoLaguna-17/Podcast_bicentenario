import { Component,Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import { NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-gestion-podcasts',
  imports: [CommonModule,FormsModule],
  templateUrl: './gestion-podcasts.component.html',
  styleUrl: './gestion-podcasts.component.css'
})
export class GestionPodcastsComponent {
  podcasts:any[]=[]
  errorRespuesta:any
  mostrarModal:boolean=false
  idEditar:any
  tituloEditar:string=''
  descripcionEditar:string=''
  constructor(private router: Router,private http: HttpClient,) {
      this.listarPodcasts();
    }
  listarPodcasts(){
    const endpoint=environment.apiUrl+'/listarPodcasts/';
    this.http.get<{podcasts:any}>(endpoint).subscribe({
      next:(response)=>{
        this.podcasts=response.podcasts
        console.log(this.podcasts)
      },
      error:(error)=>{
         console.error('Error en gestion de podcasts:', error);
            this.errorRespuesta = 'Error al cargar los podcasts.';
      }
    });
  }
  editar(podcast:any){
    this.mostrarModal=true;
    this.idEditar=podcast.idpodcast;
    this.tituloEditar=podcast.titulo;
    this.descripcionEditar=podcast.descripcion;
  }
  cerrarModal(){
    this.mostrarModal=false;
    this.idEditar='';
    this.tituloEditar='';
    this.descripcionEditar='';

  }
  
 

actualizarPodcast(){
  const confirmar=window.confirm('Actualizar el podcast '+this.tituloEditar+'?' );
  if(confirmar){
    const endpoint=environment.apiUrl+'/actualizarPodcast/';
    const actualizar=new FormData()
    actualizar.append('idpodcast',this.idEditar);
    actualizar.append('titulo',this.tituloEditar);
    actualizar.append('descripcion',this.descripcionEditar);
    this.http.post(endpoint,actualizar).subscribe({
      next:(response)=>{
        alert('podcast actualizado')
        this.cerrarModal();
        this.listarPodcasts()
      },
      error:(error)=>{
        console.error('Error al actualizar podcast:', error);
        this.errorRespuesta = 'Error al actualizar podcast.';
      }
    });

  }else{
    this.cerrarModal();
  }
}


eliminarPodcast(podcast:any){
  const confirmar=window.confirm('Desea eliminar permanentemente el podcast '+podcast.titulo+'?')
  if(confirmar){
    const confirmar2=window.confirm('La siguiente accion no podra deshacerse. ¿Eliminar permanentemente el podcast '+podcast.titulo+'?');
    if(confirmar2){
      const enpoint=environment.apiUrl+'/borrarPodcast/'
      const eliminar=new FormData()
      eliminar.append('idpodcast',podcast.idpodcast)
      this.http.post(enpoint,eliminar).subscribe({
        next:(response)=>{
          alert('Podcast eliminado permanentemente')
          this.listarPodcasts()
        },
        error:(error)=>{
          console.error('Error al eliminar podcast:', error);
          this.errorRespuesta = 'Error al eliminar podcast.';
        }
      });
    }
  }
}

 

gestionarEpisodios(podcast: any) {
  this.router.navigate(['/gestion-episodios'], {
    queryParams: {
      id: podcast.idpodcast,
      titulo:podcast.titulo
    }
  });
}
}

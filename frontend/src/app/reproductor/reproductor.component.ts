import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient , HttpHeaders} from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatOptionModule } from '@angular/material/core';
import { MatIconModule } from '@angular/material/icon';
import { environment } from '../../environments/environment';
import { ListComentariosComponent } from '../list-comentarios/list-comentarios.component';
import { FormsModule } from '@angular/forms';
import { ListReseniaComponent } from '../list-resenia/list-resenia.component';
@Component({
  selector: 'app-reproductor',
  imports: [
    CommonModule,
    MatFormFieldModule,
    MatSelectModule,
    MatOptionModule,
     MatIconModule,
     ListComentariosComponent,
     FormsModule,
     ListReseniaComponent
  ],
  templateUrl: './reproductor.component.html',
  styleUrl: './reproductor.component.css'
})
export class ReproductorComponent {
  episodio:any;
  comentarios:any[]=[]
  resenias:any[]=[]
  idoyente:any
  rol:any
  comentar:string=''
  transcripcion:string=''
  puntuacion:any
  reseniar:string=''
  seguidos:any
  siguiendo:any
  errorRespuesta:any
  headers:any
  constructor( private http: HttpClient, private router: Router) {
    const token = localStorage.getItem('access_token');
  
    if (!token) {
      this.errorRespuesta = 'No se encontró token de autenticación.';
      return;
    }
    this.headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
    });

    this.episodio=this.router.getCurrentNavigation()?.extras.state?.['datos'];
    console.log('reproduciendo '+this.episodio.audio)
    const formData = new FormData();
    console.log("episodio a actualiar",this.episodio.idepisodio)
        formData.append('idepisodio', this.episodio.idepisodio);
    
        const endpoint = environment.apiUrl + '/actualizar_visualizaciones/';
        const headers=this.headers
        this.http.post(endpoint, formData,{headers}).subscribe({
          next: (response) => {
            
            console.log(response);
          },
          error: (error) => {
            console.error('Error en al actualizar vistas:', error);
          }
        });
    const usuarioStr = localStorage.getItem('usuario');
    if (usuarioStr) {
      const usuarioObj = JSON.parse(usuarioStr);
      this.rol = usuarioObj.rol; 
      this.idoyente=usuarioObj.id; // aquí está el id
      // Usar idUsuario para lo que necesites, ej. en el query param
    }
        this.obtenerTranscripcion()
        this.obtenerComentarios(this.episodio.idepisodio);
        this.obtenerResenias();
        this.verificarSeguimiento();
    
    
  }
   velocidades: number[] = [0.5, 0.75, 1, 1.25, 1.5, 2];

  cambiarVelocidad(event: any, audioPlayer: HTMLAudioElement) {
    audioPlayer.playbackRate = event.value;
  }
  obtenerTranscripcion(){
    let url=this.episodio.audio;
    let endpoint=environment.apiUrl +'/transcribir/';
    const formTranscripcion=new FormData()
    formTranscripcion.append('url',url);
    this.http.post<{ transcripcion: string }>(endpoint,formTranscripcion).subscribe({
          next: (response) => {
            
            this.transcripcion=response.transcripcion;
          },
          error: (error) => {
            console.error('Error en al obtener comentarios:', error);
          }
        });
  }
  obtenerComentarios(idvideo:any){
    const headers=this.headers
    let endpoint=environment.apiUrl +'/obtener_comentarios/?episodios_idepisodio='+idvideo;
     this.http.get<{comentarios: any[]}>(endpoint,{headers}).subscribe({
          next: (response) => {
            this.comentar='';
            this.comentarios=response.comentarios;
          },
          error: (error) => {
            console.error('Error en al obtener comentarios:', error);
          }
        });
  }

  
  comentarEpisodio(){
    let endpoint=environment.apiUrl +'/usuarios/comentar/';
    const comentario=new FormData()
    const headers=this.headers;
    comentario.append("idEpisodio",this.episodio.idepisodio);
    comentario.append("idOyente",this.idoyente);
    comentario.append("contenido",this.comentar)
     this.http.post(endpoint,comentario,{headers}).subscribe({
          next: (response) => {
           this.obtenerComentarios(this.episodio.idepisodio)
            
          },
          error: (error) => {
            console.error('Error en al obtener comentarios:', error);
          }
        });
  }

  reseniarEpisodio(){
    let endpoint=environment.apiUrl +'/usuarios/subirCalificacion/';
    const calificacion=new FormData()
    calificacion.append('idusuario',this.idoyente);
    calificacion.append('idepisodio',this.episodio.idepisodio);
    calificacion.append('puntuacion',this.puntuacion);
    calificacion.append('resenia',this.reseniar);
    const headers=this.headers
    this.http.post(endpoint,calificacion,{headers}).subscribe({
          next: (response) => {
           console.log('Reseña exitosa')
            this.obtenerResenias
          },
          error: (error) => {
            console.error('Error en calificar:', error);
          }
        });

  }
  obtenerResenias(){
  const headers=this.headers
  let endpoint=environment.apiUrl +'/obtenerCalificaciones/?episodios_idepisodio='+this.episodio.idepisodio;
  this.http.get<{resenias: any[]}>(endpoint,{headers}).subscribe({
          next: (response) => {
            
            this.resenias=response.resenias;
            console.log('calificaciones ')
          },
          error: (error) => {
            console.error('Error en al obtener resenias:', error);
          }
        });
  }
  verificarSeguimiento(){
    const idcreador=this.episodio.podcast_idpodcast.creadores_idcreador.idcreador;
    let endpoint=environment.apiUrl+'/usuarios/verificarSeguimiento/?idusuario='+this.idoyente+'&idCreador='+idcreador;
    this.http.get<{siguiendo:any}>(endpoint).subscribe({
          next: (response) => {
            
            this.siguiendo=response.siguiendo;
            console.log('sigue creador?:',this.siguiendo)
            if(this.siguiendo){
              this.seguidos='Seguido'
            }else{
              this.seguidos='Seguir'
            }
          },
          error: (error) => {
            console.error('Error en al obtener resenias:', error);
          }
        });
  }
  accionBotonSeguido(){
    if(this.siguiendo){
      const confirmar=window.confirm('¿Dejar de seguir a '+this.episodio.podcast_idpodcast.creadores_idcreador.nombre);
      if(confirmar){
        const idcreador=this.episodio.podcast_idpodcast.creadores_idcreador.idcreador;
        let endpoint=environment.apiUrl +'/usuarios/dejarSeguir/';
        const noSeguir=new FormData()
        noSeguir.append('idusuario',this.idoyente);
        noSeguir.append('idcreador',idcreador);
        this.http.post(endpoint,noSeguir).subscribe({
              next: (response) => {
              console.log('no siguiendo')
                this.verificarSeguimiento()
              },
              error: (error) => {
                console.error('Error al seguir creador:', error);
              }
            });
      }
    }else{
          const idcreador=this.episodio.podcast_idpodcast.creadores_idcreador.idcreador;
          let endpoint=environment.apiUrl +'/usuarios/seguirCreador/';
          const seguir=new FormData()
          seguir.append('usuarios_idusuario',this.idoyente);
          seguir.append('creadores_idcreador',idcreador);
          this.http.post(endpoint,seguir).subscribe({
                next: (response) => {
                console.log('Siguiendo')
                this.verificarSeguimiento()

                },
                error: (error) => {
                  console.error('Error al seguir creador:', error);
                }
              });

    }
  }
   
}

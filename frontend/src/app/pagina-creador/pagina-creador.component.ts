import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient ,HttpHeaders} from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatOptionModule } from '@angular/material/core';
import { MatIconModule } from '@angular/material/icon';
import { environment } from '../../environments/environment';
import { MatChipsModule } from '@angular/material/chips';
import { PodcastListComponent } from '../podcast-list/podcast-list.component';
@Component({
  selector: 'app-pagina-creador',
  imports: [ CommonModule,
    MatFormFieldModule,
    MatSelectModule,
    MatOptionModule,
     MatIconModule,
     MatChipsModule,
    PodcastListComponent],
  templateUrl: './pagina-creador.component.html',
  styleUrl: './pagina-creador.component.css'
})
export class PaginaCreadorComponent {
creador:any
errorRespuesta:any
idoyente:any
rol:any
  seguidos:any
  siguiendo:any
  podcasts:any[]=[]
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
    this.creador=this.router.getCurrentNavigation()?.extras.state?.['datos'];
    console.log(this.creador)
    const usuarioStr = localStorage.getItem('usuario');
    if (usuarioStr) {
      const usuarioObj = JSON.parse(usuarioStr);
      this.rol = usuarioObj.rol; 
      this.idoyente=usuarioObj.id; // aquí está el id
      // Usar idUsuario para lo que necesites, ej. en el query param
    }
    this.verificarSeguimiento()
    this.obtenerPodcast()
  }

  obtenerPodcast(){
    
    const headers = this.headers
    let endpoint=environment.apiUrl+"/creador/podcasts/?idcreador="+this.creador.idcreador;
    this.http.get<{podcasts: any[]}>(endpoint,{headers}).subscribe({
          next: (response) => {
            
            this.podcasts=response.podcasts;
          },
          error: (error) => {
            console.error('Error en al obtener podcasts:', error);
          }
        });

  }
  verificarSeguimiento(){
    const headers = this.headers
    let endpoint=environment.apiUrl+'/usuarios/verificarSeguimiento/?idusuario='+this.idoyente+'&idCreador='+this.creador.idcreador;
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
    const headers = this.headers
    if(this.siguiendo){
      const confirmar=window.confirm('¿Dejar de seguir a '+this.creador.nombre);
      if(confirmar){
        let endpoint=environment.apiUrl +'/usuarios/dejarSeguir/';
        const noSeguir=new FormData()
        noSeguir.append('idusuario',this.idoyente);
        noSeguir.append('idcreador',this.creador.idcreador);
        this.http.post(endpoint,noSeguir,{headers}).subscribe({
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
          let endpoint=environment.apiUrl +'/usuarios/seguirCreador/';
          const seguir=new FormData()
          seguir.append('usuarios_idusuario',this.idoyente);
          seguir.append('creadores_idcreador',this.creador.idcreador);
          this.http.post(endpoint,seguir,{headers}).subscribe({
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

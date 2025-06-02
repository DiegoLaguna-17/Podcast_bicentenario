import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatOptionModule } from '@angular/material/core';
import { MatIconModule } from '@angular/material/icon';
import { environment } from '../../environments/environment';
import { ListComentariosComponent } from '../list-comentarios/list-comentarios.component';
import { FormsModule } from '@angular/forms';
import { ListReseniaComponent } from '../list-resenia/list-resenia.component';
import { MatChipsModule } from '@angular/material/chips';
import { ListEpisodiosComponent } from '../list-episodios/list-episodios.component';
@Component({
  selector: 'app-pagina-podcast',
  imports: [
    CommonModule,
    MatFormFieldModule,
    MatSelectModule,
    MatOptionModule,
     MatIconModule,
     MatChipsModule,
     ListEpisodiosComponent
  ],
  templateUrl: './pagina-podcast.component.html',
  styleUrl: './pagina-podcast.component.css'
})
export class PaginaPodcastComponent {
  podcast:any
  episodios:any[]=[]
  suscrito:any
  suscripcion:any
  rol:any
  dato1:any
  dato2:any
 idoyente:any
 premium:any
 mostrarModal:boolean=false
  constructor( private http: HttpClient, private router: Router) {
    this.podcast=this.router.getCurrentNavigation()?.extras.state?.['datos'];
    console.log(this.podcast)
    const usuarioStr = localStorage.getItem('usuario');
    if (usuarioStr) {
      const usuarioObj = JSON.parse(usuarioStr);
      this.rol = usuarioObj.rol; 
      this.idoyente=usuarioObj.id; // aquí está el id
      // Usar idUsuario para lo que necesites, ej. en el query param
    }
    this.obtenerEpisodios()
    this.verificarSuscripcion()

  }
  obtenerEpisodios(){
    let endpoint=environment.apiUrl+"/podcast/episodios/?idpodcast="+this.podcast.idpodcast;
    this.http.get<{episodios: any[]}>(endpoint).subscribe({
          next: (response) => {
            
            this.episodios=response.episodios;
          },
          error: (error) => {
            console.error('Error en al obtener comentarios:', error);
          }
        });
  }
  verificarSuscripcion(){
    let endpoint=environment.apiUrl+"/usuarios/verificarSuscripcion/?idusuario="+this.idoyente+"&idpodcast="+this.podcast.idpodcast;
    this.http.get<{suscrito:any}>(endpoint).subscribe({
          next: (response) => {
            
            this.suscrito=response.suscrito;
            console.log('sigue creador?:',this.suscrito)
            if(this.suscrito){
              this.suscripcion='Suscrito'
            }else{
              this.suscripcion='Suscribirse'
            }
          },
          error: (error) => {
            console.error('Error en al obtener resenias:', error);
          }
        });
  }
  accionBotonSuscribirse(){
    if(!this.suscrito){
      this.mostrarModal=true;
      
    }
  }
  suscribirse(){
    if(!this.suscrito){
      const confirmar=window.confirm('¿Confirmar suscripcion a '+this.podcast.titulo);
        if(confirmar){
          let endpoint=environment.apiUrl +'/usuarios/suscribirse/';
          const siSuscrito=new FormData()
          siSuscrito.append('idusuario',this.idoyente);
          siSuscrito.append('idpodcast',this.podcast.idpodcast);
          this.http.post(endpoint,siSuscrito).subscribe({
                next: (response) => {
                console.log('suscrito')
                  this.verificarSuscripcion()
                },
                error: (error) => {
                  console.error('Error al suscribirse al podcast:', error);
                }
              });
        }
    }
  }
  
}

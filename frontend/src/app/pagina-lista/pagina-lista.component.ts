import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient , HttpHeaders} from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatOptionModule } from '@angular/material/core';
import { MatIconModule } from '@angular/material/icon';
import { environment } from '../../environments/environment';
import { FormsModule } from '@angular/forms';
import { MatChipsModule } from '@angular/material/chips';
import { ListEpListaComponent } from '../list-ep-lista/list-ep-lista.component';

@Component({
  selector: 'app-pagina-lista',
  imports: [
      CommonModule,
    MatFormFieldModule,
    MatSelectModule,
    MatOptionModule,
     MatIconModule,
     MatChipsModule,
     ListEpListaComponent
  ],
  templateUrl: './pagina-lista.component.html',
  styleUrl: './pagina-lista.component.css'
})
export class PaginaListaComponent {
  errorRespuesta:any
  episodios:any[]=[]
  lista:any
  constructor( private http: HttpClient, private router: Router) {
    this.lista=this.router.getCurrentNavigation()?.extras.state?.['datos'];
    localStorage.setItem('lista', JSON.stringify(this.lista));
    this.obtenerEpisodios();
  }

    obtenerEpisodios(){
        const token = localStorage.getItem('access_token');
  
    if (!token) {
      this.errorRespuesta = 'No se encontró token de autenticación.';
      return;
    }
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
    });
      let endpoint=environment.apiUrl+"/lista/obtenerepisodios/?idlista="+this.lista.idlista;
      this.http.get<{episodios: any[]}>(endpoint,{headers}).subscribe({
            next: (response) => {
              
              this.episodios=response.episodios;
              console.log
            },
            error: (error) => {
              console.error('Error en al obtener comentarios:', error);
            }
          });
    }
}

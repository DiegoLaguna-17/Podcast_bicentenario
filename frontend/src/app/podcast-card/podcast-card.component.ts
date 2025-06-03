import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { ListEpisodiosComponent } from '../list-episodios/list-episodios.component';
@Component({
  selector: 'app-podcast-card',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatChipsModule,
    MatIconModule
  ],
  templateUrl: './podcast-card.component.html',
  styleUrls: ['./podcast-card.component.css']
})
export class PodcastCardComponent {
  @Input() podcast!: any;
  suscrito:any
  rol:any
  idoyente:any
  constructor(private router: Router,private http: HttpClient,) {// { id: 1, nombre: "Ejemplo" }
     const usuarioStr = localStorage.getItem('usuario');
    if (usuarioStr) {
      const usuarioObj = JSON.parse(usuarioStr);
      this.rol = usuarioObj.rol; 
      this.idoyente=usuarioObj.id; // aquí está el id
      // Usar idUsuario para lo que necesites, ej. en el query param
    }
    }
  abrirPodcast(podcast: any){
    
      this.router.navigate(['/podcast'],{
        state: {datos:podcast}
      });
    
  }
  
}
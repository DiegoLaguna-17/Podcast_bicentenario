import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-card-episodios',
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatChipsModule,
    MatIconModule
  ],
  templateUrl: './card-episodios.component.html',
  styleUrl: './card-episodios.component.css'
})
export class CardEpisodiosComponent {
@Input ()episodio:any
  suscrito:any
  rol:any
  idoyente:any
  premium:any
  podcast:any
  constructor(private router: Router,private http: HttpClient,) {// { id: 1, nombre: "Ejemplo" }
    }
  abrirReproductor(episodio: any){
    
      this.router.navigate(['/reproductor'],{
          state: {datos:episodio}
        });
    
    
  }
  
}

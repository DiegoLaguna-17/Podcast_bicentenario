import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';


@Component({
  selector: 'app-card-episodios',
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatChipsModule,
    MatIconModule,
    RouterLink,
  ],
  templateUrl: './card-episodios.component.html',
  styleUrl: './card-episodios.component.css'
})
export class CardEpisodiosComponent {
@Input ()episodio:any
  constructor(private router: Router) {// { id: 1, nombre: "Ejemplo" }
    }
  abrirReproductor(episodio: any){
    this.router.navigate(['/reproductor'],{
      state: {datos:episodio}
    });
  }
}

import { Component,Input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';

import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';
@Component({
  selector: 'app-card-creadores',
  imports: [MatButtonModule,MatCardModule,MatChipsModule,MatIconModule,RouterLink],
  templateUrl: './card-creadores.component.html',
  styleUrl: './card-creadores.component.css'
})
export class CardCreadoresComponent {
@Input ()creador:any
constructor(private router: Router) {// { id: 1, nombre: "Ejemplo" }
    }
  abrirCreador(creador: any){
    this.router.navigate(['/creador'],{
      state: {datos:creador}
    });
  }
}

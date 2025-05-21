import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-card-comentarios',
  imports: [
    
  ],
  templateUrl: './card-comentarios.component.html',
  styleUrl: './card-comentarios.component.css'
})
export class CardComentariosComponent {
@Input ()comentarios:any
  constructor(private router: Router){}
  abrirCajaCOmentarios(comentarios:any){
    this.router.navigate(['/reproductor'], {state: {datos: comentarios}});
  }
}

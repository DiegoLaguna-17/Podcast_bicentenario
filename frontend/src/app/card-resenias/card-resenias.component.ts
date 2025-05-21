import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-card-resenias',
  imports: [],
  templateUrl: './card-resenias.component.html',
  styleUrl: './card-resenias.component.css'
})
export class CardReseniasComponent {
@Input ()resenias:any
  constructor(private router: Router){}
  abrirCajaCOmentarios(resenias:any){
    this.router.navigate(['/reproductor'], {state: {datos: resenias}});
  }
}

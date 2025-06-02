import { Component,Input } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { CardComentariosComponent } from '../card-comentarios/card-comentarios.component';
@Component({
  selector: 'app-list-comentarios',
  imports: [MatIconModule,CardComentariosComponent],
  templateUrl: './list-comentarios.component.html',
  styleUrl: './list-comentarios.component.css'
})
export class ListComentariosComponent {
@Input ()comentarios:any[]=[]
}

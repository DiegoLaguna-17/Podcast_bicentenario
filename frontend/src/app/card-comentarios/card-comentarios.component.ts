import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-card-comentarios',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatIconModule,
    DatePipe
  ],
  templateUrl: './card-comentarios.component.html',
  styleUrls: ['./card-comentarios.component.css']
})
export class CardComentariosComponent {
  @Input() comentario: any;
}
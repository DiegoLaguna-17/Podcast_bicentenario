import { HttpClient } from '@angular/common/http';
import { Component, Input } from '@angular/core';
import { environment } from '../../environments/environment';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CardComentariosComponent } from '../card-comentarios/card-comentarios.component';

@Component({
  selector: 'app-comentarios',
  standalone: true,
  imports: 
  [
    CommonModule, FormsModule, CardComentariosComponent
  ],
  templateUrl: './comentarios.component.html',
  styleUrl: './comentarios.component.css'
})
export class ComentariosComponent {
 @Input() episodioId!: number;
  comentarios: any[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.cargarComentarios();
  }

  cargarComentarios(): void {
    const endpoint = `${environment.apiUrl}/comentarios/${this.episodioId}`;
    this.http.get(endpoint).subscribe({
      next: (data: any) => {
        this.comentarios = data;
      },
      error: (err) => {
        console.error('Error al cargar comentarios', err);
      },
    });
  }

}

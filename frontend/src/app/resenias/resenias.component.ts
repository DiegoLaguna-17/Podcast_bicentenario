import { HttpClient } from '@angular/common/http';
import { Component, Input } from '@angular/core';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-resenias',
  imports: [],
  templateUrl: './resenias.component.html',
  styleUrl: './resenias.component.css'
})
export class ReseniasComponent {
@Input() episodioId!: number;
  resenias: any[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.cargarResenias();
  }

  cargarResenias(): void {
    const endpoint = `${environment.apiUrl}/reseñas/${this.episodioId}`;
    this.http.get(endpoint).subscribe({
      next: (data: any) => {
        this.resenias = data;
      },
      error: (err) => {
        console.error('Error al cargar reseñas', err);
      },
    });
  }
}

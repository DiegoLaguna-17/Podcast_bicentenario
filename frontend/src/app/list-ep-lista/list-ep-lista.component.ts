import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { CardEpListaComponent } from '../card-ep-lista/card-ep-lista.component';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-list-ep-lista',
  standalone: true,
  imports: [
    CommonModule,
    CardEpListaComponent,
    MatProgressSpinnerModule,
    MatButtonModule,
    MatIconModule,
  ],
  templateUrl: './list-ep-lista.component.html',
  styleUrl: './list-ep-lista.component.css'
})
export class ListEpListaComponent implements OnInit, OnChanges {
  isLoading = true;
  error: string | null = null;

  @Input() episodios: any[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    // Ya no haces nada aquí porque los datos llegan después
  }

  esperar(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async ngOnChanges(changes: SimpleChanges) {
    if (changes['episodios']) {
      // Espera un momento por si llegan datos
      await this.esperar(1000);  // Puedes ajustar el tiempo

      if (this.episodios && this.episodios.length > 0) {
        this.isLoading = false;
      } else {
        // Si sigue vacío luego de esperar, también quitamos el loading
        this.isLoading = false;
      }
    }
  }
}

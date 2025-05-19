import { Component, Input, OnInit  } from '@angular/core';

import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { CardEpisodiosComponent } from '../card-episodios/card-episodios.component';
import { HttpClient , HttpHeaders} from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-list-episodios',
  imports: [
    CommonModule,
    CardEpisodiosComponent,
    MatProgressSpinnerModule,
    MatButtonModule,
    MatIconModule
  ],
  templateUrl: './list-episodios.component.html',
  styleUrl: './list-episodios.component.css'
})
export class ListEpisodiosComponent {

  episodios: any[] = [];
  isLoading = false;
  error: string | null = null;
  
  constructor(private  http: HttpClient) {}

  ngOnInit(): void {
    this.isLoading=true;
    this.loadEpisodios();

  }

  loadEpisodios(): void {
    const token = localStorage.getItem('access_token');
  
        
        const headers = new HttpHeaders({
          'Authorization': `Bearer ${token}`,
        });
    this.error = null;
     const endpoint = environment.apiUrl + '/episodios/';
      this.http.get<{episodios: any[]}>(endpoint,{headers}).subscribe({
        next: (response) => {
          console.log(response);
          this.episodios= response.episodios || [];
          console.log('episodios  '+this.episodios);
          this.isLoading=false;
          // Aquí marcamos que los datos han sido cargados
        },
        error: (error) => {
          console.error('Error en el perfil:', error);

        }
      });
    
  }

  

}

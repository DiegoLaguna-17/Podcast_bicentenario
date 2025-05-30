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

  isLoading = false;
  error: string | null = null;
  @Input ()episodios:any[]=[]
  constructor(private  http: HttpClient) {}

/*
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
    var idUsuario=''
    const usuarioStr = localStorage.getItem('usuario');
    if (usuarioStr) {
      const usuarioObj = JSON.parse(usuarioStr);
      idUsuario = usuarioObj.id;  // aquí está el id
      console.log('ID usuario:', idUsuario);
      // Usar idUsuario para lo que necesites, ej. en el query param
    }
     const endpoint = environment.apiUrl + '/episodios/?idusuario='+idUsuario;
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
*/
  

}

import { Component } from '@angular/core';
import { DataService } from '../DataService';
import { NgIf } from '@angular/common';
import { HttpClient,HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import {ListEpisodiosComponent} from '../list-episodios/list-episodios.component';
@Component({
  selector: 'app-para-ti',
  imports: [ListEpisodiosComponent],
  templateUrl: './para-ti.component.html',
  styleUrl: './para-ti.component.css'
})

export class ParaTiComponent {
 episodios: any[] = [];
  isLoading = false;
  error: string | null = null;

  mensajeRespuesta: string | null = null;
  errorRespuesta: string | null = null;
  datos: any;
  id: any;
  rol:any
  datosCargados: boolean = false; // Bandera para controlar si los datos están cargados

  constructor(private dataService: DataService, private http: HttpClient, private router: Router) {
      
     
  }

  
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
    console.log('token',token);
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

  

}

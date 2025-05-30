import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Router } from '@angular/router';
import {DataService} from '../DataService';
import { NgIf } from '@angular/common';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';



@Component({
  standalone: true,
  selector: 'app-menu-principal',
  imports: [RouterLink,NgIf, CommonModule],
  templateUrl: './menu-principal.component.html',
  styleUrl: './menu-principal.component.css'
})

export class MenuPrincipalComponent {
  respuesta: any
  usuario:  any
  vistasTotales:any
  episodioVisto:any
  seguidores:any
  errorRespuesta:any
    constructor(private router: Router,private dataService: DataService,private http: HttpClient,) {
    this.usuario = JSON.parse(localStorage.getItem('usuario') || '{}');
    console.log('llego a menu: '+this.usuario.id+" "+this.usuario.rol); // { id: 1, nombre: "Ejemplo" }

    if(this.usuario.rol=='Creador'){
      this.dashBoardCreador()
    }
  }

  dashBoardCreador(){
    console.log(this.usuario.id)
    this.obtenerVistasTotales()
    this.obtenerEpisodioMasVisto()
    this.obtenerConteoSeguidores()
  }
  obtenerConteoSeguidores(){
    const endpoint = environment.apiUrl + '/obtenerConteoSeguidores/'+'?idcreador='+this.usuario.id;
        this.http.get(endpoint).subscribe({
          next: (response:any) => {
            this.seguidores=response['Cantidad de seguidores']
          },
          error: (error) => {
            console.error('Error en el perfil:', error);
            this.errorRespuesta = 'Error al cargar el perfil.';
          }
        });
  }
  obtenerEpisodioMasVisto(){
    const endpoint = environment.apiUrl + '/obtenerMasVisto/'+'?idcreador='+this.usuario.id;
        
    
        this.http.get(endpoint).subscribe({
          next: (response:any) => {
          
            
            this.episodioVisto=response['episodio mas visto']
          },
          error: (error) => {
            console.error('Error en el perfil:', error);
            this.errorRespuesta = 'Error al cargar el perfil.';
          }
        });
  }
  obtenerVistasTotales(){
    const endpoint = environment.apiUrl + '/obtenerVistasCreador/'+'?idcreador='+this.usuario.id;
        this.http.get(endpoint).subscribe({
          next: (response:any) => {
          
            this.vistasTotales=response['Vistas del creador']
            console.log(this.vistasTotales)
          },
          error: (error) => {
            console.error('Error en el perfil:', error);
            this.errorRespuesta = 'Error al cargar el perfil.';
          }
        });
  }
  enviarPerfil(){
    this.router.navigate(['/perfil'], {
          state: { datos: this.usuario } // Envías un objeto completo
        });
  }
  enviarSiguiendo(){
    this.router.navigate(['/siguiendo'], {
          state: { datos: this.usuario.id } // Envías un objeto completo
        });
  }
  subirEpisodio(){
    console.log('enviando a subir '+this.usuario.id)
    this.router.navigate(['/subir-episodio'], {
          state: { datos: this.usuario.id } // Envías un objeto completo
        });
  }
  
}

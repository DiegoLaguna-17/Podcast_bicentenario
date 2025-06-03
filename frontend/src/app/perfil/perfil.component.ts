import { Component } from '@angular/core';
import { NgIf } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { PodcastListComponent } from '../podcast-list/podcast-list.component';

@Component({
  selector: 'app-perfil',
  imports: [NgIf, PodcastListComponent],
  templateUrl: './perfil.component.html',
  styleUrls: ['./perfil.component.css'] // Cambiado a styleUrls (plural) y array
})
export class PerfilComponent {
  mensajeRespuesta: string | null = null;
  errorRespuesta: string | null = null;
  datosper: any;
  id: any;
  rol: any;
  datosCargados: boolean = false;
  podcasts:any[]=[]

  rolUsuario:any
  isLoading = true;
  error: string | null = null;

  constructor(private http: HttpClient, private router: Router) {
    const datosend = JSON.parse(localStorage.getItem('usuario') || '{}');

    if (!datosend) {
      this.errorRespuesta = 'No se recibió información del usuario.';
      return;
    }

    console.log('llego al perfil ' + datosend.id + ' ' + datosend.rol);

    // Prepara los datos para enviar (puedes usar JSON porque el backend espera POST)
      const formData = new FormData();
      formData.append('id', datosend.id);
      formData.append('rol', datosend.rol);

    // Obtén token y arma headers con HttpHeaders para mayor compatibilidad
    const token = localStorage.getItem('access_token');
  
    if (!token) {
      this.errorRespuesta = 'No se encontró token de autenticación.';
      return;
    }
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
    });

    const endpoint = environment.apiUrl + '/perfil/';
    

    this.http.post(endpoint, formData, { headers }).subscribe({
      next: (response) => {
        console.log(response);
        this.datosper = response;
        this.id = this.datosper.id;
        this.rol = this.datosper.rol;
        
        console.log(this.datosper.fotoperfil);
        console.log('id del perfil: ' + this.id + ' ' + this.rol);
        this.datosCargados = true;
      },
      error: (error) => {
        console.error('Error en el perfil:', error);
        this.errorRespuesta = 'Error al cargar el perfil.';
      }
    });

    const usuarioStr = localStorage.getItem('usuario');
    if (usuarioStr) {
      const usuarioObj = JSON.parse(usuarioStr);
      this.rolUsuario = usuarioObj.rol;  // aquí está el id
      // Usar idUsuario para lo que necesites, ej. en el query param
    }
    if(this.rolUsuario=='Creador'){
      this.loadPodcasts();
    }
  }
  subirPubli(){
    this.router.navigate(['/subir-publicidad']);
  }

  loadPodcasts(): void {
    const token = localStorage.getItem('access_token');
  
        
        const headers = new HttpHeaders({
          'Authorization': `Bearer ${token}`,
        });
    this.isLoading = true;
    this.error = null;

    var idUsuario=''
    const usuarioStr = localStorage.getItem('usuario');
    if (usuarioStr) {
      const usuarioObj = JSON.parse(usuarioStr);
      idUsuario = usuarioObj.id;  // aquí está el id
      console.log('ID usuario:', idUsuario);
      // Usar idUsuario para lo que necesites, ej. en el query param
    }
    const endpoint = environment.apiUrl+'/creador/podcasts/?idcreador='+idUsuario;
    this.http.get<{podcasts: any[]}>(endpoint,{headers}).subscribe({
      next: (response) => {
         this.podcasts = response.podcasts || [];
         console.log('podcasts del creador: ',this.podcasts);
      },
      error: (error) => {
        console.error('Error en el perfil:', error);
      }
        
    });
    
  }
  cerrarSesion(){
    this.router.navigate(['/login']);
  }
}

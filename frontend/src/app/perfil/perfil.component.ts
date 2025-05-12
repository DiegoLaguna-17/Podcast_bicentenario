import { Component, OnInit, OnDestroy } from '@angular/core';
import { DataService } from '../DataService';
import { NgIf } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';

@Component({
  selector: 'app-perfil',
  imports: [NgIf],
  templateUrl: './perfil.component.html',
  styleUrl: './perfil.component.css'
})
export class PerfilComponent {
  mensajeRespuesta: string | null = null;
  errorRespuesta: string | null = null;
  datosend: any;
  datosper:any
  id: any;
  rol:any
  datosCargados: boolean = false; // Bandera para controlar si los datos están cargados

  constructor(private dataService: DataService, private http: HttpClient, private router: Router) {
    this.datosend=this.router.getCurrentNavigation()?.extras.state?.['datos'];
      console.log('llego al perfil' +this.datosend.id);
      const  formData=new FormData();
      formData.append('id', this.datosend.id);
      formData.append('rol', this.datosend.rol);
      const endpoint = environment.apiUrl + '/perfil/';
      this.http.post(endpoint, formData).subscribe({
        next: (response) => {
          console.log(response);
          this.datosper = response;
          this.id = this.datosper.id;
          this.rol=this.datosper.rol
          console.log('id del perfil: ' + this.id+' '+this.rol);
          
          // Aquí marcamos que los datos han sido cargados
          this.datosCargados = true;
        },
        error: (error) => {
          console.error('Error en el perfil:', error);
        }
      });
  }

  subirEpisodio(){
    console.log('enviando a subir '+this.id)
    this.router.navigate(['/subir-episodio'], {
          state: { datos: this.id } // Envías un objeto completo
        });
  }
}
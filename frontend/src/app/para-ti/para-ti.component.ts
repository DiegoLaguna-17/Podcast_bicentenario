import { Component } from '@angular/core';
import { DataService } from '../DataService';
import { NgIf } from '@angular/common';
import { HttpClient } from '@angular/common/http';
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

  mensajeRespuesta: string | null = null;
  errorRespuesta: string | null = null;
  datos: any;
  id: any;
  rol:any
  datosCargados: boolean = false; // Bandera para controlar si los datos están cargados

  constructor(private dataService: DataService, private http: HttpClient, private router: Router) {
      
     
  }
  

}

import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-subir-publicidades',
  templateUrl: './subir-publicidades.component.html',
  styleUrls: ['./subir-publicidades.component.css']
})
export class SubirPublicidadesComponent {
  publicidad = {
    nombre: '',
    imagen: null as File | null
  };
  
  
}
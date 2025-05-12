import { Component } from '@angular/core';
import { DataService } from '../DataService';
import { NgIf } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-siguiendo',
  imports: [CommonModule],
  templateUrl: './siguiendo.component.html',
  styleUrl: './siguiendo.component.css'
})
export class SiguiendoComponent {
   idusuario: any
   siguiendo: any[]=[]
   creadores: any[]=[]
   constructor(private router: Router,private dataService: DataService,private http: HttpClient) {
    this.idusuario = this.router.getCurrentNavigation()?.extras.state?.['datos'];
    console.log('llego a siguiendo: '+this.idusuario); // { id: 1, nombre: "Ejemplo" }
    const endpoint = environment.apiUrl+'/usuarios/obtenerSeguimientos/'+'?usuarios_idusuario='+this.idusuario;
    this.http.get<{siguiendo: any[]}>(endpoint).subscribe({
        next: (response) => {
           this.siguiendo = response.siguiendo || [];
           console.log('Seguidos por '+this.idusuario+':', this.siguiendo);
          
            this.siguiendo.forEach(item=>{
                  const endpoint = environment.apiUrl+'/creador/'+'?creadores_idcreador='+item.creadores_idcreador;
                  this.http.get<{creador: any[]}>(endpoint).subscribe({
                next: (response) => {
                  this.creadores=response.creador ||[];
                  
                },
                error: (error) => {
                  console.error('Error en el perfil:', error);
                }
              });

            });
        },
        error: (error) => {
          console.error('Error en el perfil:', error);
        }
        
      });
      

  }
 

}

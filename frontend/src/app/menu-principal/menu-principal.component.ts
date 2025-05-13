import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Router } from '@angular/router';
import {DataService} from '../DataService';
import { NgIf } from '@angular/common';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-menu-principal',
  imports: [RouterLink,NgIf, CommonModule],
  templateUrl: './menu-principal.component.html',
  styleUrl: './menu-principal.component.css'
})
export class MenuPrincipalComponent {
  usuario: any
  
   constructor(private router: Router,private dataService: DataService,) {
    this.usuario = this.router.getCurrentNavigation()?.extras.state?.['datos'];
    console.log('llego a menu: '+this.usuario.id+' '+this.usuario.rol); // { id: 1, nombre: "Ejemplo" }
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

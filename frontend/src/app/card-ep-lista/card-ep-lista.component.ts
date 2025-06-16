import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';
import { environment } from '../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
@Component({
  selector: 'app-card-ep-lista',
  imports: [
     CommonModule,
    MatCardModule,
    MatButtonModule,
    MatChipsModule,
    MatIconModule
  ],
  templateUrl: './card-ep-lista.component.html',
  styleUrl: './card-ep-lista.component.css'
})
export class CardEpListaComponent {
@Input ()episodio:any
errorRespuesta:any
constructor(private router: Router,private http: HttpClient,) {// { id: 1, nombre: "Ejemplo" }
    }
  abrirReproductor(episodio: any){
    
      this.router.navigate(['/reproductor'],{
          state: {datos:episodio}
        });
    
    
  }
  quitarEpisodio(episodio:any){
    const lista = JSON.parse(localStorage.getItem('lista') || '{}');
    const confirmar=window.confirm('Desea quitar este episodio de la lista '+lista.titulo+'?')
    if(confirmar){
       const token = localStorage.getItem('access_token');
  
    if (!token) {
      this.errorRespuesta = 'No se encontró token de autenticación.';
      return;
    }
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
    });
      const endpoint=environment.apiUrl+"/usuarios/quitarEpisodioLista/";
      const quitar=new FormData
      quitar.append('idepisodio',episodio.idepisodio)
      quitar.append('idLista',lista.idlista)
      
      this.http.post(endpoint,quitar,{headers}).subscribe({
         next: (response) => {
              alert(response)
              window.location.reload();

            },
            error: (error) => {
              console.error('Error en al quitar episodio:', error);
            }
      });
    }


  }
}

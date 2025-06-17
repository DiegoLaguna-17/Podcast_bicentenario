import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';
import { environment } from '../../environments/environment';
import { HttpClient , HttpHeaders} from '@angular/common/http';

@Component({
  selector: 'app-card-lista',
  imports: [
     CommonModule,
    MatCardModule,
    MatButtonModule,
    MatChipsModule,
    MatIconModule
  ],
  templateUrl: './card-lista.component.html',
  styleUrl: './card-lista.component.css'
})
export class CardListaComponent {
@Input ()lista:any
errorRespuesta:any
headers:any
 constructor(private router: Router,private http: HttpClient,) {
  const token = localStorage.getItem('access_token');
  
    if (!token) {
      this.errorRespuesta = 'No se encontró token de autenticación.';
      return;
    }
    this.headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
    });
 }
abrirLista(lista:any){
   this.router.navigate(['/lista'],{
        state: {datos:lista}
      });
}

borrarLista(lista:any){
  const confirmar=window.confirm('Borrar la lista de reproduccion?' );
  if(confirmar){
    const endpoint=environment.apiUrl+'/usuarios/borrarLista/?idLista='+lista.idlista;
    const headers=this.headers
    this.http.get<{mensaje:string}>(endpoint,{headers}).subscribe({
      next:(response)=>{
        alert('Lista eliminada con exito')
        window.location.reload();
      },
      error:(error)=>{
        alert("Error al borrar lista")
      }
    })
  }

}
}

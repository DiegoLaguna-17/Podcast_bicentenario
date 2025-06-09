import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { environment } from '../../environments/environment';
@Component({
  selector: 'app-subir-podcast',
  imports: [FormsModule],
  templateUrl: './subir-podcast.component.html',
  styleUrl: './subir-podcast.component.css'
})
export class SubirPodcastComponent {
podcast = {
  titulo: '',
  descripcion: '',
  categoria: '',
  primium: ''
};
errorRespuesta:any
headers:any
   constructor(private http: HttpClient) {
    const token = localStorage.getItem('access_token');
  
    if (!token) {
      this.errorRespuesta = 'No se encontró token de autenticación.';
      return;
    }
    this.headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
    });
   }
subirPodcast() {
  const usuario = JSON.parse(localStorage.getItem('usuario') || '{}');
  const datos = new FormData();
  datos.append('creador',usuario.id)
  datos.append('titulo', this.podcast.titulo);
  datos.append('descripcion', this.podcast.descripcion);
  datos.append('categoria', this.podcast.categoria);
  datos.append('premium', this.podcast.primium);
  const endpoint=environment.apiUrl+'/podcast/'
  const headers=this.headers
  // Enviar al backend
  this.http.post(endpoint, datos,{headers}).subscribe({
    next: res => {
      alert('Podcast subido con éxito')
      this.podcast.titulo=''
      this.podcast.descripcion=''
      this.podcast.categoria=''
      this.podcast.primium=''
    },
    error: err => alert('Error al subir podcast')
  });
}

}

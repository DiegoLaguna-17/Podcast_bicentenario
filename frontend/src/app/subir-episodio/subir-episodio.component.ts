import { Component, OnDestroy,HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import {DataService} from '../DataService';
import {Router} from '@angular/router';
import { HttpClient,HttpHeaders } from '@angular/common/http'; 
import { environment } from '../../environments/environment';
import { Location } from '@angular/common';


@Component({
  selector: 'app-subir-episodio',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './subir-episodio.component.html',
  styleUrls: ['./subir-episodio.component.css']
})
export class SubirEpisodioComponent implements OnDestroy{
  audioFile: File | null = null;
  audioUrl: string | null = null;
  mensajeRespuesta: string | null = null;
  errorRespuesta: string | null = null;
  datosend:any
podcasts: any[] = [];
  episode = {
  title: '',
  podcast_id: '',
  descripcion: '',
  participantes: '',
  fecha: ''
};
cargando=false
minDate: string = '';

ngOnInit() {
  this.minDate = this.obtenerFechaLocal();
}

obtenerFechaLocal(): string {
  const now = new Date();
  now.setSeconds(0, 0);
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hour = String(now.getHours()).padStart(2, '0');
  const minute = String(now.getMinutes()).padStart(2, '0');
  return `${year}-${month}-${day}T${hour}:${minute}`;
}


 onFileSelected(event: any) {
  this.audioUrl = null;
  setTimeout(() => {
    const file: File = event.target.files[0];
    if (file) {
      this.audioFile = file;

      if (this.audioUrl) {
        URL.revokeObjectURL(this.audioUrl);
      }

      this.audioUrl = URL.createObjectURL(file);
    }
  }, 100);
}


  onSubmit(form: NgForm) {
    const token = localStorage.getItem('access_token');
  
        if (!token) {
          this.errorRespuesta = 'No se encontró token de autenticación.';
          return;
        }
        const headers = new HttpHeaders({
          'Authorization': `Bearer ${token}`,
        });
    if (this.audioFile && form.valid) {
       const formData = new FormData();
      // Aquí iría la lógica para subir el video 
      if (this.episode.fecha < this.minDate) {
        alert('La fecha y hora deben ser actuales o futuras.');
        return;
      }
      console.log('podcast id:', this.episode.podcast_id);
      console.log('titulo:', this.episode.title);
      console.log('descripcion:', this.episode.descripcion);
      console.log('Fecha enviada:', this.episode.fecha);
      console.log('participantes:', this.episode.participantes);

      formData.append('podcast', this.episode.podcast_id);
      formData.append('titulo', this.episode.title);
      formData.append('descripcion', this.episode.descripcion);
      formData.append('fecha', this.episode.fecha);
      formData.append('audio', this.audioFile);
      formData.append('participantes', this.episode.participantes);
      this.cargando=true;
      const endpoint = environment.apiUrl + '/episodio/';
      this.http.post(endpoint, formData,{headers}).subscribe({
        next: (response) => {
          console.log(response);
          this.cargando=false;
          alert('episodio publicado')
           form.resetForm(); // <-- esto limpia el NgForm
          this.audioFile = null;
          this.episode = {
            podcast_id: '',
            title: '',
            descripcion: '',
            fecha: '',
            participantes: ''
          };
          this.audioUrl=null;
          this.audioFile=null;
          const inaudio=document.getElementById('audioFile')as HTMLInputElement;;
          if(inaudio){
            inaudio.value='';
          }
          
            
          
          
          
        },
        error: (error) => {
          console.error('Error en el perfil:', error);
        }
      });
    }
      
  }

  ngOnDestroy() {
    // Liberar la URL cuando el componente se destruye
    if (this.audioUrl) {
      URL.revokeObjectURL(this.audioUrl);
    }
  }
  constructor(private dataService: DataService,private http: HttpClient,private router: Router,private location:Location) {
        const token = localStorage.getItem('access_token');
  
        if (!token) {
          this.errorRespuesta = 'No se encontró token de autenticación.';
          return;
        }
        const headers = new HttpHeaders({
          'Authorization': `Bearer ${token}`,
        });
        const usuario = JSON.parse(localStorage.getItem('usuario') || '{}');
        this.datosend=usuario.id;
        console.log('llego a subir ep '+this.datosend);
        const formData=new FormData();
        formData.append('id',this.datosend);
        const endpoint = environment.apiUrl+'/creador/podcasts/';
        this.http.post<{podcasts: any[]}>(endpoint, formData,{headers}).subscribe({
        next: (response) => {
           this.podcasts = response.podcasts || [];
           console.log('Podcasts cargados:', this.podcasts);
  
          // Aquí marcamos que los datos han sido cargados
          
        },
        error: (error) => {
          console.error('Error en el perfil:', error);
        }
      });
      


  }
  @HostListener('window:popstate', ['$event'])
  onPopState(event: any) {
    // Acción personalizada cuando se presiona la flecha atrás
    console.log('Flecha atrás presionada', event);
    
    // Evitar que el usuario regrese a la página anterior
    this.router.navigate(['/menu-principal']);
  }
  irAtras() {
    this.location.back();
  }

}

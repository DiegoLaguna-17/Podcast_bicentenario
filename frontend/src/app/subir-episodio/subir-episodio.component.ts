import { Component, OnDestroy,HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import {DataService} from '../DataService';
import {Router} from '@angular/router';
import { HttpClient } from '@angular/common/http'; 
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
  premium: false,
  podcast_id: '',
  descripcion: '',
  participantes: '',
  fecha: ''
};


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
    console.log(this.datosend);
    
    if (this.audioFile && form.valid) {
       const formData = new FormData();
      // Aquí iría la lógica para subir el video 
      formData.append('podcast', this.episode.podcast_id);
      formData.append('titulo', this.episode.title);
      formData.append('descripcion', this.episode.descripcion);
      formData.append('fecha', this.episode.fecha);
      formData.append('audio', this.audioFile);
      formData.append('participantes', this.episode.participantes);
      const endpoint = environment.apiUrl + '/episodio/';
      this.http.post(endpoint, formData).subscribe({
        next: (response) => {
          console.log(response);

          
          
          // Aquí marcamos que los datos han sido cargados
          
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
        this.datosend=this.router.getCurrentNavigation()?.extras.state?.['datos'];
        console.log('llego a subir ep '+this.datosend);
        const formData=new FormData();
        formData.append('id',this.datosend);
        const endpoint = environment.apiUrl+'/creador/podcasts/';
        this.http.post<{podcasts: any[]}>(endpoint, formData).subscribe({
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

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatOptionModule } from '@angular/material/core';
import { MatIconModule } from '@angular/material/icon';
import { environment } from '../../environments/environment';


@Component({
  selector: 'app-reproductor',
  imports: [
    CommonModule,
    MatFormFieldModule,
    MatSelectModule,
    MatOptionModule,
     MatIconModule,
  ],
  templateUrl: './reproductor.component.html',
  styleUrl: './reproductor.component.css'
})
export class ReproductorComponent {
  episodio:any;
  constructor( private http: HttpClient, private router: Router) {
    this.episodio=this.router.getCurrentNavigation()?.extras.state?.['datos'];
    console.log('reproduciendo '+this.episodio.audio)
    const formData = new FormData();
    console.log("episodio a actualiar",this.episodio.idepisodio)
        formData.append('idepisodio', this.episodio.idepisodio);
    
        const endpoint = environment.apiUrl + '/actualizar_visualizaciones/';
    
        this.http.post(endpoint, formData).subscribe({
          next: (response) => {
            
    
          },
          error: (error) => {
            console.error('Error en al actualizar vistas:', error);
          }
        });

    
  }
   velocidades: number[] = [0.5, 0.75, 1, 1.25, 1.5, 2];

  cambiarVelocidad(event: any, audioPlayer: HTMLAudioElement) {
    audioPlayer.playbackRate = event.value;
  }
   
}

import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { PodcastCardComponent } from '../podcast-card/podcast-card.component';
import { HttpClient ,HttpHeaders} from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-podcast-list',
  standalone: true,
  imports: [
    CommonModule,
    PodcastCardComponent,
    MatProgressSpinnerModule,
    MatButtonModule,
    MatIconModule
  ],
  templateUrl: './podcast-list.component.html',
  styleUrls: ['./podcast-list.component.css']
})
export class PodcastListComponent  {
  @Input() podcasts: any[] = []; // Valor por defecto o recíbelo desde un padre
  
  
  isLoading = true;
  error: string | null = null;
  
  constructor(private  http: HttpClient) {}
/*
  ngOnInit(): void {
    console.log(this.creadorId);
    this.loadPodcasts();
  }

  loadPodcasts(): void {
    const token = localStorage.getItem('access_token');
  
        
        const headers = new HttpHeaders({
          'Authorization': `Bearer ${token}`,
        });
    this.isLoading = true;
    this.error = null;
    const formData =new FormData();
    let creador=this.creadorId;
    formData.append('id',creador);
    const endpoint = environment.apiUrl+'/creador/podcasts/';
    this.http.post<{podcasts: any[]}>(endpoint,formData,{headers}).subscribe({
      next: (response) => {
         this.podcasts = response.podcasts || [];
         console.log(this.podcasts);
      },
      error: (error) => {
        console.error('Error en el perfil:', error);
      }
        
    });
    
  }
    */
}
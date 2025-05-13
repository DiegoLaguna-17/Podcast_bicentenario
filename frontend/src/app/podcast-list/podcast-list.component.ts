import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { PodcastCardComponent } from '../podcast-card/podcast-card.component';
import { HttpClient } from '@angular/common/http';
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
export class PodcastListComponent implements OnInit {
  @Input() creadorId!: any; // Valor por defecto o recíbelo desde un padre
  
  podcasts: any[] = [];
  isLoading = true;
  error: string | null = null;
  
  constructor(private  http: HttpClient) {}

  ngOnInit(): void {
    console.log(this.creadorId);
    this.loadPodcasts();
  }

  loadPodcasts(): void {

    this.isLoading = true;
    this.error = null;
    const formData =new FormData();
    let creador=this.creadorId;
    formData.append('id',creador);
    const endpoint = environment.apiUrl+'/creador/podcasts/';
    this.http.post<{podcasts: any[]}>(endpoint,formData).subscribe({
      next: (response) => {
         this.podcasts = response.podcasts || [];
         console.log(this.podcasts);
      },
      error: (error) => {
        console.error('Error en el perfil:', error);
      }
        
    });
    
  }
}
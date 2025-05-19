import { Component, OnInit } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { HttpClient } from '@angular/common/http';

interface PodcastData {
  id: number;
  titulo: string;
  premium: boolean;
  creadores_idcreador: number;
  creator_name?: string;
  upload_date?: string;
  duration?: string;
  tematicas?: string[];
  thumbnail_url?: string;
}

@Component({
  selector: 'app-buscar',
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './buscar.component.html',
  styleUrl: './buscar.component.css'
})
export class BuscarComponent implements OnInit {
  podcasts: PodcastData[] = [];
  private apiUrl = '/'; // De aqui se jalan los podcasts

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.fetchPodcasts();
  }

  fetchPodcasts(): void {
    this.http.get<PodcastData[]>(this.apiUrl).subscribe(
      (data) => {
        this.podcasts = data;
        console.log('Podcasts fetched:', this.podcasts);
      },
      (error) => {
        console.error('Error fetching podcasts:', error);
      }
    );
  }
}
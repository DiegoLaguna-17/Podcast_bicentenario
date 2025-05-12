import { Component, Input, OnInit } from '@angular/core';
import { PodcastService } from '../../services/podcast.service';
import { Podcast } from '../../models/podcast.model';
import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { PodcastCardComponent } from '../podcast-card/podcast-card.component';

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
  @Input() creatorId: number = 1; // Valor por defecto o recíbelo desde un padre
  
  podcasts: Podcast[] = [];
  isLoading = true;
  error: string | null = null;

  constructor(private podcastService: PodcastService) {}

  ngOnInit(): void {
    this.loadPodcasts();
  }

  loadPodcasts(): void {
    this.isLoading = true;
    this.error = null;
    
    this.podcastService.getPodcastsByCreator(this.creatorId).subscribe({
      next: (response) => {
        this.podcasts = response.podcasts || [];
        this.isLoading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar los podcasts';
        this.isLoading = false;
        console.error('Error loading podcasts:', err);
      }
    });
  }
}
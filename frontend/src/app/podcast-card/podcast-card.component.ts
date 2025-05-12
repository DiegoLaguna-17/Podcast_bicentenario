import { Component, Input } from '@angular/core';
import { Podcast } from '../../models/podcast.model';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { TruncatePipe } from '../../pipes/truncate.pipe'; 

@Component({
  selector: 'app-podcast-card',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatChipsModule,
    MatIconModule,
    TruncatePipe
  ],
  templateUrl: './podcast-card.component.html',
  styleUrls: ['./podcast-card.component.css']
})
export class PodcastCardComponent {
  @Input() podcast!: Podcast;
}
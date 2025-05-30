import { Component ,Input} from '@angular/core';
import { CardCreadoresComponent } from '../card-creadores/card-creadores.component';
import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { PodcastCardComponent } from '../podcast-card/podcast-card.component';
import { HttpClient ,HttpHeaders} from '@angular/common/http';
import { environment } from '../../environments/environment';
@Component({
  selector: 'app-list-creadores',
  imports: [CardCreadoresComponent,
    CommonModule,
    MatProgressSpinnerModule,
    MatButtonModule,
    MatIconModule
  ],
  templateUrl: './list-creadores.component.html',
  styleUrl: './list-creadores.component.css'
})
export class ListCreadoresComponent {
   
  isLoading = true;
  error: string | null = null;
@Input ()creadores:any[]=[]
}

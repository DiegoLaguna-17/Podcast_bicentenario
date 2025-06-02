import { Component, Input, OnInit  } from '@angular/core';

import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { HttpClient , HttpHeaders} from '@angular/common/http';
import { environment } from '../../environments/environment';
import { CardReseniaComponent } from '../card-resenia/card-resenia.component';
@Component({
  selector: 'app-list-resenia',
  imports: [CommonModule,
      CardReseniaComponent,
      MatProgressSpinnerModule,
      MatButtonModule,
      MatIconModule],
  templateUrl: './list-resenia.component.html',
  styleUrl: './list-resenia.component.css'
})
export class ListReseniaComponent {
  isLoading = false;
  error: string | null = null;
  @Input ()resenias:any[]=[]

}

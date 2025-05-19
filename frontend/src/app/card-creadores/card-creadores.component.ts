import { Component,Input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
@Component({
  selector: 'app-card-creadores',
  imports: [MatButtonModule,MatCardModule,MatChipsModule,MatIconModule],
  templateUrl: './card-creadores.component.html',
  styleUrl: './card-creadores.component.css'
})
export class CardCreadoresComponent {
@Input ()creador:any
}

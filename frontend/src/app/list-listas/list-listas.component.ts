import { Component, Input, OnInit  } from '@angular/core';
import { CardListaComponent } from '../card-lista/card-lista.component';
import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
@Component({
  selector: 'app-list-listas',
  imports: [
    CommonModule,
        CardListaComponent,
        MatProgressSpinnerModule,
        MatButtonModule,
        MatIconModule
  ],
  templateUrl: './list-listas.component.html',
  styleUrl: './list-listas.component.css'
})

export class ListListasComponent {
@Input ()listas:any[]=[]
isLoading:any
error:any
 constructor( ) {
   
    localStorage.setItem('lista', '');
  }
}

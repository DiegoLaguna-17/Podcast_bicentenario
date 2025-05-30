import { Component, OnInit } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { FormsModule } from '@angular/forms';
import { PodcastListComponent } from '../podcast-list/podcast-list.component';
import { ListCreadoresComponent } from '../list-creadores/list-creadores.component';
import { ListEpisodiosComponent } from '../list-episodios/list-episodios.component';
import { CommonModule } from '@angular/common';
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
  imports: [RouterLink, RouterLinkActive,FormsModule,ListEpisodiosComponent,ListCreadoresComponent, PodcastListComponent,CommonModule],
  templateUrl: './buscar.component.html',
  styleUrl: './buscar.component.css'
})
export class BuscarComponent implements OnInit {
  cargando:boolean=false
  podcasts: any[] = [];
  creadores:any[]=[]
  episodios:any[]=[]
  textoBusqueda: string = '';
  porAnio: boolean = false;
  porTematica: boolean = false;
  mostrarGeneral: boolean = true;
  sinResultados:boolean=false;
  filtroActivo: string = 'Busqueda general';
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


  buscar(){
    this.cargando=true
    this.creadores=[]
    this.podcasts=[]
    this.episodios=[]
    const busqueda=this.textoBusqueda;
    this.sinResultados=false;
    if(this.mostrarGeneral){
      const endpoint = environment.apiUrl + '/buscar_general/?q='+busqueda;
            this.http.get<{episodios: any[],podcasts:any[],creadores:any[]}>(endpoint).subscribe({
              next: (response) => {
                console.log(response);
                this.cargando=false
                this.episodios= response.episodios || [];
                this.podcasts=response.podcasts ||[];
                this.creadores=response.creadores||[];

                console.log('Podcasts encontrados:', this.podcasts);
                console.log('Episodios encontrados:', this.episodios);
                console.log('Creadores encontrados:', this.creadores);
                if(this.creadores.length==0 && this.episodios.length==0 && this.podcasts.length==0 ){
                  this.sinResultados=true;
                  
                }
                
                // Aquí marcamos que los datos han sido cargados
              },
              error: (error) => {
                console.error('Error en el perfil:', error);
      
              }
            });
    }else if(this.porTematica){
      const endpoint=environment.apiUrl + '/buscar_tematica/?q='+busqueda;
      this.http.get<{episodios: any[],podcasts:any[],creadores:any[]}>(endpoint).subscribe({
              next: (response) => {
                this.cargando=false
                console.log(response);
                this.episodios= response.episodios || [];
                this.podcasts=response.podcasts ||[];
                this.creadores=response.creadores||[];
                console.log('Podcasts encontrados:', this.podcasts);
                console.log('Episodios encontrados:', this.episodios);
                console.log('Creadores encontrados:', this.creadores);
                if(this.creadores.length==0 && this.episodios.length==0 && this.podcasts.length==0 ){
                  this.sinResultados=true;
                }
                // Aquí marcamos que los datos han sido cargados
              },
              error: (error) => {
                console.error('Error en el perfil:', error);
      
              }
            });
    }
    else if(this.porAnio && !isNaN(parseInt(this.textoBusqueda))){
      const endpoint=environment.apiUrl + '/buscar_anio/?q='+busqueda;
      this.http.get<{episodios: any[],podcasts:any[],creadores:any[]}>(endpoint).subscribe({
              next: (response) => {
                this.cargando=false
                console.log(response);
                this.episodios= response.episodios || [];
                this.podcasts=response.podcasts ||[];
                this.creadores=response.creadores||[];
                console.log('Podcasts encontrados:', this.podcasts);
                console.log('Episodios encontrados:', this.episodios);
                console.log('Creadores encontrados:', this.creadores);
                if(this.creadores.length==0 && this.episodios.length==0 && this.podcasts.length==0 ){
                  this.sinResultados=true;
                }
                // Aquí marcamos que los datos han sido cargados
              },
              error: (error) => {
                console.error('Error en el perfil:', error);
      
              }
            });

      
    }else{
      alert('Dato no valido para busqueda por año');
      this.textoBusqueda='';
    }

    
  }
  activarFiltro(tipo: string): void {
  this.porAnio = false;
  this.porTematica = false;
  this.mostrarGeneral = false;

  switch (tipo) {
    case 'anio':
      this.porAnio = true;
      this.filtroActivo='Busqueda por año'
      break;
    case 'tematica':
      this.porTematica = true;
      this.filtroActivo='Busqueda por tematica'

      break;
    case 'general':
      this.mostrarGeneral = true;
      this.filtroActivo='Busqueda general'

      break;
    // puedes añadir más filtros si es necesario
  }
}


}
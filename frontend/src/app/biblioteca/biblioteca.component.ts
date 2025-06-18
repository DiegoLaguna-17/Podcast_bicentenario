import { Component } from '@angular/core';
import { ListListasComponent } from '../list-listas/list-listas.component';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-biblioteca',
  standalone: true,
  imports: [ListListasComponent, CommonModule, FormsModule],
  templateUrl: './biblioteca.component.html',
  styleUrl: './biblioteca.component.css'
})
export class BibliotecaComponent {
  errorRespuesta: any;
  listas: any[] = [];
  usuario: any;
  titulo: string = '';
  modal: boolean = false;
  isLoading: boolean = true;

  constructor(private http: HttpClient, private router: Router) {
    this.usuario = JSON.parse(localStorage.getItem('usuario') || '{}');
    const token = localStorage.getItem('access_token');

    if (!token) {
      this.errorRespuesta = 'No se encontró token de autenticación.';
      this.isLoading = false;
      return;
    }

    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
    });

    const endpoint = environment.apiUrl + "/usuarios/obtenerlistas/?idusuario=" + this.usuario.id;

    this.http.get<{ listas: any[] }>(endpoint, { headers }).subscribe({
      next: async (response) => {
        // espera artificial para que se vea el spinner si va muy rápido
        await this.esperar(1000);
        this.listas = response.listas;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error al obtener listas:', error);
        this.isLoading = false;
      }
    });
  }

  volverAMenuPrincipal() {
    this.router.navigate(['/menu-principal']);
  }

  crearLista() {
    const token = localStorage.getItem('access_token');

    if (!token) {
      this.errorRespuesta = 'No se encontró token de autenticación.';
      return;
    }

    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
    });

    const endpoint = environment.apiUrl + "/usuarios/crearLista/";
    const form = new FormData();
    form.append('idusuario', this.usuario.id);
    form.append('tituloLista', this.titulo);

    this.http.post(endpoint, form, { headers }).subscribe({
      next: () => {
        alert('Lista creada');
        window.location.reload();
      },
      error: () => {
        alert('Error al crear lista');
      }
    });
  }

  mostrarModal() {
    this.modal = true;
  }

  cerrarModal() {
    this.modal = false;
  }

  esperar(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

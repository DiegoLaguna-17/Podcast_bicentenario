import { Component } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-verificar',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './verificar.component.html',
  styleUrls: ['./verificar.component.css']
})
export class VerificarComponent {
  codigo_verificacion: string = '';
  usuario: string = '';
  errorMessage: string = '';

  constructor(private http: HttpClient, private router: Router) {
    const correoGuardado = localStorage.getItem('usuarioVerificar');
    if (correoGuardado) {
      this.usuario = correoGuardado;
    } else {
      alert('No se encontró el usuario. Vuelva a iniciar sesión.');
      this.router.navigate(['/login']);
    }
  }

  verificarCodigo() {
    const formData = new HttpParams()
      .set('usuario', this.usuario)
      .set('codigo_verificacion', this.codigo_verificacion);

    this.http.post<any>('http://localhost:8000/verificar-codigo/', formData)
      .subscribe({
        next: () => {
          alert('Verificación exitosa. Bienvenido.');
          localStorage.removeItem('usuarioVerificar');
          this.router.navigate(['/home']);
        },
        error: (error) => {
          this.errorMessage = error.error?.error || 'Error al verificar el código.';
        }
      });
  }
}

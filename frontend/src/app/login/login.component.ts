import { Component, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  @ViewChild('loginForm') loginForm!: NgForm;
  showPassword = false;
  isLoading = false;

  constructor(
    private http: HttpClient, 
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    localStorage.clear();
  }

  usuario: any;

  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }

  showToast(message: string, isSuccess: boolean): void {
    this.snackBar.open(message, 'Cerrar', {
      duration: 3000,
      panelClass: isSuccess ? ['success-toast'] : ['error-toast'],
      horizontalPosition: 'center',
      verticalPosition: 'top'
    });
  }

  redirectBasedOnRole(role: string): void {
    switch(role) {
      case 'Oyente':
        this.router.navigate(['/para-ti']);
        break;
      case 'Creador':
        this.router.navigate(['/perfil']);
        break;
      default:
        this.router.navigate(['/menu-principal']);
    }
  }

  onSubmit() {
    if (this.loginForm.invalid) {
      return;
    }

    this.isLoading = true;

    const formData = new FormData();
    formData.append('usuario', this.loginForm.value.usuario);
    formData.append('contrasenia', this.loginForm.value.contrasenia);
    formData.append('rol', this.loginForm.value.rol);

    const endpoint = environment.apiUrl + '/login/';

    this.http.post(endpoint, formData).subscribe({
      next: (response) => {
        const res = response as { access: string; usuario: any };
        this.usuario = res.usuario;
        localStorage.setItem('access_token', res.access);
        localStorage.setItem('usuario', JSON.stringify(res.usuario));
        
        this.showToast('Inicio de sesión exitoso', true);
        this.redirectBasedOnRole(res.usuario.rol);
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error en el login:', error);
        this.showToast('Error en el inicio de sesión. Verifica tus credenciales.', false);
        this.isLoading = false;
      }
    });
  }
}
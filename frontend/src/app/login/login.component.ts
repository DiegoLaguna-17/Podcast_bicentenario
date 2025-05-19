import { Component, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';

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

  constructor(private http: HttpClient, private router: Router) {
    localStorage.clear();
  }
usuario:any
  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }

  onSubmit() {
    if (this.loginForm.invalid) {
      return;
    }

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
        this.router.navigate(['/menu-principal']);

      },
      error: (error) => {
        console.error('Error en el login:', error);
      }
    });
  }
}
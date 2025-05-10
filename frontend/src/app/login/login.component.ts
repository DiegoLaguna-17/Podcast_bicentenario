import { Component, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http'; // Importa HttpClient
import { CommonModule } from '@angular/common'; // Necesario para *ngIf, etc., en el template
import { FormsModule, NgForm } from '@angular/forms'; // Necesario para (ngSubmit), ngModel, y #registroForm="ngForm"
import { environment } from '../../environments/environment';
@Component({
  selector: 'app-login',
  standalone: true, // Marcamos el componente como standalone
  imports: [
    CommonModule,     // Para directivas como *ngIf
    FormsModule       // Para funcionalidades de formularios como ngModel y (ngSubmit)
    // HttpClientModule no se importa aquí directamente en Angular 15+ con provideHttpClient()
  ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'] // Corregido a styleUrls (plural y array)
})
export class LoginComponent {
  // ViewChild para acceder al formulario y a los inputs de archivo
  @ViewChild('loginForm') loginForm!: NgForm;
  // Variable para mensajes de éxito o error
  mensajeRespuesta: string | null = null;
  errorRespuesta: string | null = null;

  // Inyecta HttpClient en el constructor
  constructor(private http: HttpClient) {}

  onSubmit() {
    this.mensajeRespuesta = null; // Limpiar mensajes previos
    this.errorRespuesta = null;

    if (this.loginForm.invalid) {
      this.errorRespuesta = 'El formulario no es válido. Por favor, revisa los campos.';
      // Marcar todos los campos como "touched" para mostrar errores de validación si no lo están
      Object.values(this.loginForm.controls).forEach(control => {
        control.markAsTouched();
      });
      return;
    }

    // Crea un objeto FormData para enviar los datos, incluyendo archivos
    const formData = new FormData();

    // Agrega los campos de texto del formulario
    formData.append('usuario', this.loginForm.value.usuario);
    formData.append('contrasenia', this.loginForm.value.contrasenia);
    formData.append('rol', this.loginForm.value.rol);



    const endpoint = environment.apiUrl+'/login/'; 


    this.http.post(endpoint, formData).subscribe({
      next: (response) => {
        console.log('Login exitoso:', response);
        this.mensajeRespuesta = '¡Login exitoso!';
        this.loginForm.resetForm();

        
      },
      error: (error) => {
        console.error('Error en el login:', error);
        if (error.error && typeof error.error === 'object') {

          let detallesError = '';
          for (const key in error.error) {
            if (Object.prototype.hasOwnProperty.call(error.error, key)) {
              detallesError += `${key}: ${Array.isArray(error.error[key]) ? error.error[key].join(', ') : error.error[key]}\n`;
            }
          }
          this.errorRespuesta = `Error al iniciar sesion. Detalles:\n${detallesError}`;
        } else if (error.message) {
          this.errorRespuesta = `Error al iniciar sesion: ${error.message}`;
        } else {
          this.errorRespuesta = 'Ocurrió un error desconocido al iniciar sesion.';
        }
      }
    });
  }
}
import { Component, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http'; // Importa HttpClient
import { CommonModule } from '@angular/common'; // Necesario para *ngIf, etc., en el template
import { FormsModule, NgForm } from '@angular/forms'; // Necesario para (ngSubmit), ngModel, y #registroForm="ngForm"
import { environment } from '../../environments/environment';
@Component({
  selector: 'app-registrar',
  standalone: true, // Marcamos el componente como standalone
  imports: [
    CommonModule,     // Para directivas como *ngIf
    FormsModule       // Para funcionalidades de formularios como ngModel y (ngSubmit)
    // HttpClientModule no se importa aquí directamente en Angular 15+ con provideHttpClient()
  ],
  templateUrl: './registrar.component.html',
  styleUrls: ['./registrar.component.css'] // Corregido a styleUrls (plural y array)
})
export class RegistrarComponent {
  // ViewChild para acceder al formulario y a los inputs de archivo
  @ViewChild('registroForm') registroForm!: NgForm;
  @ViewChild('fotoperfil') fotoperfilInput!: ElementRef<HTMLInputElement>;
  @ViewChild('imgdonaciones') imgdonacionesInput!: ElementRef<HTMLInputElement>;

  // Variable para mensajes de éxito o error
  mensajeRespuesta: string | null = null;
  errorRespuesta: string | null = null;

  // Inyecta HttpClient en el constructor
  constructor(private http: HttpClient) {}

  onSubmit() {
    this.mensajeRespuesta = null; // Limpiar mensajes previos
    this.errorRespuesta = null;

    if (this.registroForm.invalid) {
      this.errorRespuesta = 'El formulario no es válido. Por favor, revisa los campos.';
      // Marcar todos los campos como "touched" para mostrar errores de validación si no lo están
      Object.values(this.registroForm.controls).forEach(control => {
        control.markAsTouched();
      });
      return;
    }

    // Crea un objeto FormData para enviar los datos, incluyendo archivos
    const formData = new FormData();

    // Agrega los campos de texto del formulario
    formData.append('usuario', this.registroForm.value.usuario);
    formData.append('contrasenia', this.registroForm.value.contrasenia);
    formData.append('nombre', this.registroForm.value.nombre);
    formData.append('correo', this.registroForm.value.correo);
    formData.append('biografia', this.registroForm.value.biografia);

    // Agrega los archivos
    const fotoPerfilFile = this.fotoperfilInput.nativeElement.files?.[0];
    const imgDonacionesFile = this.imgdonacionesInput.nativeElement.files?.[0];

    if (fotoPerfilFile) {
      formData.append('fotoperfil', fotoPerfilFile);
    } else {
      
      this.errorRespuesta = 'La foto de perfil es requerida.';
      return;
    }

    if (imgDonacionesFile) {
      formData.append('imgdonaciones', imgDonacionesFile);
    } else {
      this.errorRespuesta = 'La imagen de donaciones es requerida.';
      return;
    }


    const endpoint = environment.apiUrl+'/registro/'; 


    this.http.post(endpoint, formData).subscribe({
      next: (response) => {
        console.log('Registro exitoso:', response);
        this.mensajeRespuesta = '¡Usuario registrado exitosamente!';
        this.registroForm.resetForm();

        if (this.fotoperfilInput) this.fotoperfilInput.nativeElement.value = '';
        if (this.imgdonacionesInput) this.imgdonacionesInput.nativeElement.value = '';
      },
      error: (error) => {
        console.error('Error en el registro:', error);
        if (error.error && typeof error.error === 'object') {

          let detallesError = '';
          for (const key in error.error) {
            if (Object.prototype.hasOwnProperty.call(error.error, key)) {
              detallesError += `${key}: ${Array.isArray(error.error[key]) ? error.error[key].join(', ') : error.error[key]}\n`;
            }
          }
          this.errorRespuesta = `Error al registrar el usuario. Detalles:\n${detallesError}`;
        } else if (error.message) {
          this.errorRespuesta = `Error al registrar el usuario: ${error.message}`;
        } else {
          this.errorRespuesta = 'Ocurrió un error desconocido al registrar el usuario.';
        }
      }
    });
  }
}
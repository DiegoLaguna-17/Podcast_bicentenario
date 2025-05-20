import { Component, ViewChild,ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-registrar',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './registrar.component.html',
  styleUrls: ['./registrar.component.css']
})
export class RegistrarComponent {
  selectedUserType: 'Oyente' | 'Creador' | 'Administrador' = 'Oyente';
  showPassword = false;
  @ViewChild('creadorfotoPerfil') creadorFotoperfilInput!: ElementRef<HTMLInputElement>;
  @ViewChild('creadorimagenDonaciones') creadorImgdonacionesInput!: ElementRef<HTMLInputElement>;
  extension:any
  // Modelos para cada tipo de usuario
  oyente = {
    usuario: '',
    contrasenia: '',
    correo: '',
    fotoPerfil: null as File | null,
    fotoPerfilPreview: ''
  };

  creador = {
    usuario: '',
    contrasenia: '',
    correo: '',
    nombre: '',
    biografia: '',
    fotoPerfil: null as File | null,
    imagenDonaciones: null as File | null,
    fotoPerfilPreview: '',
    imagenDonacionesPreview: ''
  };

  administrador = {
    usuario: '',
    contrasenia: '',
    correo: '',
    fotoPerfil: null as File | null,
    fotoPerfilPreview: ''
  };

  // Variables para mensajes de respuesta
  mensajeRespuesta: string | null = null;
  errorRespuesta: string | null = null;

  constructor(private http: HttpClient) {}

  // Maneja el cambio de archivos para todos los tipos de usuario
  onFileChange(event: any, field: string, userType: string) {
    const file = event.target.files[0];
    if (!file) return;

    // Crear vista previa de la imagen
    const reader = new FileReader();
    reader.onload = () => {
      if (userType === 'oyente') {
        this.oyente.fotoPerfilPreview = reader.result as string;
      } else if (userType === 'creador') {
        if (field === 'fotoPerfil') {
          this.creador.fotoPerfilPreview = reader.result as string;
        } else if (field === 'imagenDonaciones') {
          this.creador.imagenDonacionesPreview = reader.result as string;
        }
      } else if (userType === 'administrador') {
        this.administrador.fotoPerfilPreview = reader.result as string;
      }
    };
    reader.readAsDataURL(file);

    // Asignar el archivo al modelo correspondiente
    if (userType === 'oyente') {
      this.oyente.fotoPerfil = file;
    } else if (userType === 'creador') {
      if (field === 'fotoPerfil') {
        this.creador.fotoPerfil = file;
      } else if (field === 'imagenDonaciones') {
        this.creador.imagenDonaciones = file;
      }
    } else if (userType === 'administrador') {
      this.administrador.fotoPerfil = file;
    }
  }

  // Envío del formulario para Oyente
  onSubmitOyente(form: NgForm) {
    if (form.invalid) {
      this.mostrarError('Por favor, completa todos los campos requeridos.');
      return;
    }

    if (!this.oyente.fotoPerfil) {
      this.mostrarError('La foto de perfil es requerida.');
      return;
    }

    const formData = new FormData();
    formData.append('usuario', this.oyente.usuario);
    formData.append('contrasenia', this.oyente.contrasenia);
    formData.append('correo', this.oyente.correo);
    formData.append('fotoPerfil', this.oyente.fotoPerfil);
    formData.append('tipoUsuario', 'Oyente');
    this.extension='usuario'
    this.enviarRegistro(formData, form);
  }

  // Envío del formulario para Creador
  onSubmitCreador(form: NgForm) {
    if (form.invalid) {
      this.mostrarError('Por favor, completa todos los campos requeridos.');
      return;
    }

    if (!this.creador.fotoPerfil) {
      this.mostrarError('La foto de perfil es requerida.');
      return;
    }

    if (!this.creador.imagenDonaciones) {
      this.mostrarError('La imagen para donaciones es requerida.');
      return;
    }
    
    const formData = new FormData();
    formData.append('usuario', this.creador.usuario);
    formData.append('contrasenia', this.creador.contrasenia);
    formData.append('correo', this.creador.correo);
    formData.append('nombre', this.creador.nombre);
    formData.append('biografia', this.creador.biografia);
    formData.append('fotoperfil',this.creador.fotoPerfil);
    formData.append('imgdonaciones',this.creador.imagenDonaciones);
    this.extension='creador'

    formData.append('tipoUsuario', 'Creador');

    this.enviarRegistro(formData, form);
  }

  // Envío del formulario para Administrador
  onSubmitAdministrador(form: NgForm) {
    if (form.invalid) {
      this.mostrarError('Por favor, completa todos los campos requeridos.');
      return;
    }

    if (!this.administrador.fotoPerfil) {
      this.mostrarError('La foto de perfil es requerida.');
      return;
    }

    const formData = new FormData();
    formData.append('usuario', this.administrador.usuario);
    formData.append('contrasenia', this.administrador.contrasenia);
    formData.append('correo', this.administrador.correo);
    formData.append('fotoPerfil', this.administrador.fotoPerfil);
    formData.append('tipoUsuario', 'Administrador');
    this.extension='usuario'

    this.enviarRegistro(formData, form);
  }

  // Método común para enviar el registro
  private enviarRegistro(formData: FormData, form: NgForm) {
    this.mensajeRespuesta = null;
    this.errorRespuesta = null;

    const endpoint = environment.apiUrl + '/registro/'+this.extension+'/';

    this.http.post(endpoint, formData).subscribe({
      next: (response) => {
        console.log('Registro exitoso:', response);
        this.mensajeRespuesta = `¡Usuario registrado exitosamente como ${formData.get('tipoUsuario')}!`;
        this.resetForm(form);
      },
      error: (error) => {
        console.error('Error en el registro:', error);
        this.procesarError(error);
      }
    });
  }

  // Método para resetear el formulario
  private resetForm(form: NgForm) {
    form.resetForm();
    if (this.selectedUserType === 'Oyente') {
      this.oyente = {
        usuario: '',
        contrasenia: '',
        correo: '',
        fotoPerfil: null,
        fotoPerfilPreview: ''
      };
    } else if (this.selectedUserType === 'Creador') {
      this.creador = {
        usuario: '',
        contrasenia: '',
        correo: '',
        nombre: '',
        biografia: '',
        fotoPerfil: null,
        imagenDonaciones: null,
        fotoPerfilPreview: '',
        imagenDonacionesPreview: ''
      };
    } else if (this.selectedUserType === 'Administrador') {
      this.administrador = {
        usuario: '',
        contrasenia: '',
        correo: '',
        fotoPerfil: null,
        fotoPerfilPreview: ''
      };
    }
  }

  // Método para mostrar errores
  private mostrarError(mensaje: string) {
    this.errorRespuesta = mensaje;
  }

  // Método para procesar errores del servidor
  private procesarError(error: any) {
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
}
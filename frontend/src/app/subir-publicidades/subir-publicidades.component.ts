import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-subir-publicidades',
  templateUrl: './subir-publicidades.component.html',
  styleUrls: ['./subir-publicidades.component.css'],
  imports:[CommonModule,FormsModule]
})
export class SubirPublicidadesComponent {
 publicidad = {
    nombre: ''
  };

  selectedFile: File | null = null;
  selectedFileName: string = '';
  imagePreview: string | ArrayBuffer | null = null;

  constructor(private http: HttpClient) {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      this.selectedFileName = this.selectedFile.name;

      const reader = new FileReader();
      reader.onload = () => {
        this.imagePreview = reader.result;
      };
      reader.readAsDataURL(this.selectedFile);
    }
  }

  formValid(): boolean {
    return this.publicidad.nombre.trim() !== '' && !!this.selectedFile;
  }

  subirPublicidad(): void {
    if (!this.formValid()) {
      alert('Completa todos los campos');
      return;
    }

    const formData = new FormData();
    formData.append('nombrePublicidad', this.publicidad.nombre);
    if (this.selectedFile) {
      formData.append('fotoPublicidad', this.selectedFile);
    }
    const endpoint=environment.apiUrl+'/subirPublicidad/'
    this.http.post(endpoint, formData).subscribe({
      next: (res) => {
        console.log('Publicidad subida con éxito:', res);
        alert('Publicidad subida correctamente');
        this.resetFormulario();
      },
      error: (err) => {
        console.error('Error al subir publicidad:', err);
        alert('Hubo un error al subir la publicidad');
      }
    });
  }

  resetFormulario(): void {
    this.publicidad.nombre = '';
    this.selectedFile = null;
    this.selectedFileName = '';
    this.imagePreview = null;
  }
}
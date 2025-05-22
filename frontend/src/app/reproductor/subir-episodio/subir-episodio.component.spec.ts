import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';

@Component({
  selector: 'app-subir-episodio',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './subir-episodio.component.html',
  styleUrls: ['./subir-episodio.component.css']
})
export class SubirEpisodioComponent {
  episode = {
    titulo: '',
    descripcion: '',
    fechaPublicacion: '',
    audio: null as File | null,
    participantes: ''
  };

  onFileChange(event: Event, field: string) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      this.episode.audio = input.files[0];
    }
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  onSubmit(form: NgForm) {
    if (form.invalid) return;
    
    const formData = new FormData();
    formData.append('titulo', this.episode.titulo);
    formData.append('descripcion', this.episode.descripcion);
    formData.append('fechaPublicacion', this.episode.fechaPublicacion);
    formData.append('participantes', this.episode.participantes);
    if (this.episode.audio) {
      formData.append('audio', this.episode.audio);
    }

    console.log('Datos del episodio:', formData);
    // Aquí iría la llamada HTTP para subir el episodio
  }
}
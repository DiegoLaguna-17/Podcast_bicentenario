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

  constructor(private http: HttpClient) {}
  publicidad = {
    nombre: '',
    imagen: null as File | null
  };
  selectedFileName:any
  imagePreview:any
  selectedFile:any
  subirPublicidad(){
    const enpoint=environment.apiUrl+'/subirPublicidad/';
    const subir=new FormData()
    subir.append('nombrePublicidad',this.publicidad.nombre)
    subir.append('fotoPublicidad',this.selectedFile)
    this.http.post(enpoint,subir).subscribe({
      next:(response)=>{
        alert('Publicidad subida')
      },
      error:(error)=>{
        alert('error al subir publicidad')
      }
    });
  }
  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.selectedFileName = file.name;

      // Vista previa de la imagen
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.imagePreview = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }

  formValid(): boolean {
    return this.publicidad.nombre.trim() !== '' && this.selectedFile !== null;
  }
  
}
import { Component,Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import { NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-gestion-creadores',
  imports: [CommonModule,FormsModule],
  templateUrl: './gestion-creadores.component.html',
  styleUrl: './gestion-creadores.component.css'
})
export class GestionCreadoresComponent {
  creadores:any[]=[]
  errorRespuesta:any
  mostrarModal:boolean=false
  idEditar:any
  usuarioEditar:string=''
  nombreEditar:string=''
  biografiaEditar:string=''
  telefonoEditar:string=''
  imagen:any
  imagenSeleccionada:any
  donaciones:any
  imagenDon:any
  cargando:boolean=false;
  headers:any
  constructor(private router: Router,private http: HttpClient,) {
    const token = localStorage.getItem('access_token');
  
    if (!token) {
      this.errorRespuesta = 'No se encontró token de autenticación.';
      return;
    }
    this.headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
    });
      this.listarCreadores();
    }
  listarCreadores(){
    this.cargando=true;
    const headers=this.headers
    const endpoint=environment.apiUrl+'/creadores/listar/';
    this.http.get<{creadores:any}>(endpoint,{headers}).subscribe({
      next:(response)=>{
        this.creadores=response.creadores
        console.log(this.creadores)
        this.cargando=false;
      },
      error:(error)=>{
         console.error('Error en gestion de creadores:', error);
            this.errorRespuesta = 'Error al cargar los creadores.';
      }
    });
  }
  editar(creador:any){
    this.mostrarModal=true;
    this.idEditar=creador.idcreador;
    this.usuarioEditar=creador.usuario;
    this.nombreEditar=creador.nombre;
    this.biografiaEditar=creador.biografia;
    this.telefonoEditar=creador.telefono;
    this.imagen=creador.fotoperfil;
    this.donaciones=creador.imgdonaciones;

  }
  cerrarModal(){
    this.mostrarModal=false;
    this.idEditar='';
    this.usuarioEditar='';
    this.nombreEditar='';
    this.biografiaEditar='';
    this.telefonoEditar='';
    this.imagen='';
    this.donaciones='';

  }
  
  onFileSelected(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    this.imagenSeleccionada = target.files[0];
    
    const reader = new FileReader();
    reader.onload = () => {
      this.imagen = reader.result;  // aquí guardamos el base64 o data URL
    };
    reader.readAsDataURL(this.imagenSeleccionada);
  }
}
onFileSelected2(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    this.imagenDon = target.files[0];
    
    const reader = new FileReader();
    reader.onload = () => {
      this.donaciones = reader.result;  // aquí guardamos el base64 o data URL
    };
    reader.readAsDataURL(this.imagenDon);
  }
}

actualizarCreador(){
  const confirmar=window.confirm('Actualiza perfil de '+this.usuarioEditar+'?' );
  if(confirmar){
    const headers=this.headers
    const endpoint=environment.apiUrl+'/actualizarCreador/';
    const actualizar=new FormData()
    actualizar.append('idcreador',this.idEditar);
    actualizar.append('usuario',this.usuarioEditar);
    actualizar.append('nombre',this.nombreEditar);
    actualizar.append('biografia',this.biografiaEditar);
    actualizar.append('telefono',this.telefonoEditar);
    if (this.imagenSeleccionada) {
      actualizar.append('fotoperfil', this.imagenSeleccionada);
    }

    if (this.imagenDon) {
      actualizar.append('imgdonaciones', this.imagenDon);
    }
    this.http.post(endpoint,actualizar,{headers}).subscribe({
      next:(response)=>{
        alert('Creador actualizado')
        this.cerrarModal();
        this.listarCreadores()
      },
      error:(error)=>{
        console.error('Error al actualizar creador:', error);
        this.errorRespuesta = 'Error al actualizar perfil.';
      }
    });

  }else{
    this.cerrarModal();
  }
}

eliminarCreador(creador:any){
  const confirmar=window.confirm('Desea eliminar permanentemente al creador '+creador.usuario+'?')
  if(confirmar){
    const confirmar2=window.confirm('La siguiente accion no podra deshacerse. ¿Eliminar permanentemente a '+creador.usuairo+'?');
    if(confirmar2){
      const headers=this.headers
      const enpoint=environment.apiUrl+'/borrarCreador/'
      const eliminar=new FormData()
      eliminar.append('idcreador',creador.idcreador)
      this.http.post(enpoint,eliminar,{headers}).subscribe({
        next:(response)=>{
          alert('creador eliminado permanentemente')
          this.listarCreadores()
        },
        error:(error)=>{
          console.error('Error al eliminar creador:', error);
          this.errorRespuesta = 'Error al eliminar perfil.';
        }
      });
    }
  }
}

  
}

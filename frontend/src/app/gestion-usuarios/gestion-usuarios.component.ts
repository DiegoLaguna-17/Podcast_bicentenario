import { Component,Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import { NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-gestion-usuarios',
  imports: [CommonModule,FormsModule],
  templateUrl: './gestion-usuarios.component.html',
  styleUrl: './gestion-usuarios.component.css'
})

export class GestionUsuariosComponent {
  usuarios:any[]=[]
  errorRespuesta:any
  mostrarModal:boolean=false
  idEditar:any
  usuarioEditar:string=''
  telefonoEditar:string=''
  imagen:any
  imagenSeleccionada:any
  cargando:boolean=false;
  constructor(private router: Router,private http: HttpClient,) {
      this.listarUsuarios();
    }
  listarUsuarios(){
    this.cargando=true;
    const endpoint=environment.apiUrl+'/usuarios/listar/';
    this.http.get<{usuarios:any}>(endpoint).subscribe({
      next:(response)=>{
        this.usuarios=response.usuarios
        console.log(this.usuarios)
        this.cargando=false;
      },
      error:(error)=>{
         console.error('Error en gestion de usuarios:', error);
            this.errorRespuesta = 'Error al cargar el perfil.';
      }
    });
  }
  editar(usuario:any){
    this.mostrarModal=true;
    this.idEditar=usuario.idusuario;
    console.log('id',this.idEditar);
    this.usuarioEditar=usuario.usuario;
    this.telefonoEditar=usuario.telefono;
    this.imagen=usuario.fotoperfil;

  }
  cerrarModal(){
    this.mostrarModal=false;
    this.usuarioEditar='';
    this.telefonoEditar='';
    this.imagen='';
    this.idEditar=null;

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

actualizarUsuario(){
  const confirmar=window.confirm('Actualiza perfil de '+this.usuarioEditar+'?' );
  if(confirmar){
    const endpoint=environment.apiUrl+'/usuarios/actualizarUsuario/';
    const actualizar=new FormData()
    actualizar.append('idusuario',this.idEditar);
    actualizar.append('usuario',this.usuarioEditar);
    actualizar.append('telefono',this.telefonoEditar);
    actualizar.append('fotoPerfil',this.imagenSeleccionada);
    this.http.post(endpoint,actualizar).subscribe({
      next:(response)=>{
        alert('Usuario actualizado')
        this.cerrarModal();
      },
      error:(error)=>{
        console.error('Error al actualizar usuario:', error);
        this.errorRespuesta = 'Error al actualizar perfil.';
      }
    });

  }else{
    this.cerrarModal();
  }
}

eliminarUsuario(usuario:any){
  const confirmar=window.confirm('Desea eliminar permanentemente al usuario '+usuario.usuario+'?')
  if(confirmar){
    const confirmar2=window.confirm('La siguiente accion no podra deshacerse. ¿Eliminar permanentemente a '+usuario.usuario+'?');
    if(confirmar2){
      const enpoint=environment.apiUrl+'/borrarUsuario/'
      const eliminar=new FormData()
      eliminar.append('idusuario',usuario.idusuario)
      this.http.post(enpoint,eliminar).subscribe({
        next:(response)=>{
          alert('Usuario eliminado permanentemente')
          this.listarUsuarios()
        },
        error:(error)=>{
          console.error('Error al eliminar usuario:', error);
          this.errorRespuesta = 'Error al eliminar perfil.';
        }
      });
    }
  }
}

  
}

import { Component,Input } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatOptionModule } from '@angular/material/core';
import { MatIconModule } from '@angular/material/icon';
import { environment } from '../../environments/environment';
import { ListComentariosComponent } from '../list-comentarios/list-comentarios.component';
import { FormsModule } from '@angular/forms';
import { ListReseniaComponent } from '../list-resenia/list-resenia.component';

@Component({
  selector: 'app-recuperar-contrasenia',
  imports: [
    CommonModule,
    MatFormFieldModule,
    MatSelectModule,
    MatOptionModule,
     MatIconModule,
     ListComentariosComponent,
     FormsModule,
     ListReseniaComponent
  ],
  templateUrl: './recuperar-contrasenia.component.html',
  styleUrl: './recuperar-contrasenia.component.css'
})
export class RecuperarContraseniaComponent {
correo:string=''
roles: string[] = ['Oyente', 'Creador', 'Administrador'];
rolSeleccionado:string=''
modalCodigo:boolean=false
codigo:any
validator:any
idverificar:any
rolverificar:any
modalContrasenia:boolean=false
Contrasenia1:string=''
Contrasenia2:string=''
constructor( private http: HttpClient, private router: Router) {

}
verificarCuenta(){
  const correo=new FormData()
  correo.append('correo',this.correo);
  correo.append('rol',this.rolSeleccionado)
  const endpoint=environment.apiUrl+'/usuarios/recuperarContrasenia/'
  this.http.post(endpoint, correo).subscribe({
          next: (response:any) => {
            this.idverificar=response.id
            this.validator=response.validador
            this.rolverificar=response.rol
            this.modalCodigo=true
            console.log(response);
          },
          error: (error) => {
            console.error('Error en al verficar cuenta:', error);
          }
        });
}
verificarCodigo(){
  const endpoint=environment.apiUrl+'/usuarios/verificarCodigoContrasenia/'
  const verificar=new FormData()
  verificar.append('codigo',this.codigo)
  verificar.append('validador',this.validator)
  verificar.append('id',this.idverificar)
  verificar.append('rol',this.rolverificar)
  this.http.post(endpoint,verificar).subscribe({
    next: (response:any) => {
            
            console.log(response);
            this.modalCodigo=false;
            this.modalContrasenia=true;
          },
          error: (error) => {
            console.error('Error en al averificar codigo:', error);
          }
        });
}
contraseniasCoinciden(){
  return (this.Contrasenia1==this.Contrasenia2) && this.Contrasenia1.length>0;
}
cambiarContrasenia(){
  const endpoint=environment.apiUrl+'/usuarios/cambiarContrasenia/';
  const nuevaContrasenia=new FormData()
  nuevaContrasenia.append('idusuario',this.idverificar)
  nuevaContrasenia.append('rol',this.rolverificar)
  nuevaContrasenia.append('contraseniaNueva',this.Contrasenia1)
  this.http.post(endpoint,nuevaContrasenia).subscribe({
    next: (response)=>{
      console.log(response)
      alert(response)
      this.router.navigate(['/login']);
    },
    error:(error)=>{

    }
  });

}
}

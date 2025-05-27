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
verificar: boolean= false
validator:any
idverificar:any
rolverificar:any
  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }
  verificarCodigo(codigo:HTMLInputElement){
    const cod=codigo.value
    console.log(cod)
    const form=new FormData()
    form.append('codigo',cod);
    form.append('validador',this.validator)
    form.append('id',this.idverificar)
    form.append('rol',this.rolverificar)
    const endpoint = environment.apiUrl + '/verificarCodigo/';

    this.http.post(endpoint, form).subscribe({
      next: (response) => {
        const res = response as { access: string,usuario: string};
        
        this.usuario = res.usuario;
        localStorage.setItem('access_token', res.access);
        localStorage.setItem('usuario', JSON.stringify(res.usuario));
        this.router.navigate(['/menu-principal']);
        console.log(res.access)
        console.log(res.usuario)
        

      },
      error: (error) => {
        console.error('Error en la verificacion:', error);
      }
    });
    codigo.value=''
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
        const res = response as { mensaje: string;validador: string;id:string,rol:string};
        if(res.mensaje &&res.validador){
          console.log(res.mensaje)
          this.verificar=true
          this.validator=res.validador
          this.idverificar=res.id
          this.rolverificar=res.rol

        }
        /*
        this.usuario = res.usuario;
        localStorage.setItem('access_token', res.access);
        localStorage.setItem('usuario', JSON.stringify(res.usuario));
        this.router.navigate(['/menu-principal']);
        */

      },
      error: (error) => {
        console.error('Error en el login:', error);
      }
    });
  }
}
import { Routes } from '@angular/router';
import { InicioComponent } from './inicio/inicio.component';
import { LoginComponent } from './login/login.component';
import { RegistrarComponent } from './registrar/registrar.component';
import { ParaTiComponent } from './para-ti/para-ti.component';
import { BuscarComponent } from './buscar/buscar.component';
import { SiguiendoComponent } from './siguiendo/siguiendo.component';
import { PerfilComponent } from './perfil/perfil.component';
import { MenuPrincipalComponent } from './menu-principal/menu-principal.component';
import { SubirEpisodioComponent } from './subir-episodio/subir-episodio.component';

export const routes: Routes = [
  { path: '', component: InicioComponent },
  { path: 'login', component: LoginComponent },
  { path: 'registrar', component: RegistrarComponent },
  { path: 'inicio', component: InicioComponent},
  { path: 'menu-principal', component: MenuPrincipalComponent},
  { path: 'para-ti', component: ParaTiComponent},
  { path: 'buscar', component: BuscarComponent},
  { path: 'siguiendo', component: SiguiendoComponent},
  { path: 'perfil', component: PerfilComponent},
  { path: 'subir-episodio', component: SubirEpisodioComponent}
];

import { Routes } from '@angular/router';
import { InicioComponent } from './inicio/inicio.component';
import { LoginComponent } from './login/login.component';
import { RegistrarComponent } from './registrar/registrar.component';
import { ParaTiComponent } from './para-ti/para-ti.component';
import { BuscarComponent } from './buscar/buscar.component';
import { SiguiendoComponent } from './siguiendo/siguiendo.component';
import { PerfilComponent } from './perfil/perfil.component';
import { MenuPrincipalComponent } from './menu-principal/menu-principal.component';
import { SubirEpisodioComponent } from './reproductor/subir-episodio/subir-episodio.component';
import { VerificarComponent } from './verificar/verificar.component';
import { ReproductorComponent }from './reproductor/reproductor.component';
import { PaginaPodcastComponent } from './pagina-podcast/pagina-podcast.component';
import { PaginaCreadorComponent } from './pagina-creador/pagina-creador.component';
import { RecuperarContraseniaComponent } from './recuperar-contrasenia/recuperar-contrasenia.component';
import { GestionUsuariosComponent } from './gestion-usuarios/gestion-usuarios.component';
import { GestionCreadoresComponent } from './gestion-creadores/gestion-creadores.component';
import { GestionPodcastsComponent } from './gestion-podcasts/gestion-podcasts.component';
import { GestionEpisodiosComponent } from './gestion-episodios/gestion-episodios.component';

export const routes: Routes = [
  { path: '', component: InicioComponent },
  { path: 'login', component: LoginComponent },
  { path: 'verificar',component:VerificarComponent},
  { path: 'registrar', component: RegistrarComponent },
  { path: 'inicio', component: InicioComponent},
  { path: 'menu-principal', component: MenuPrincipalComponent},
  { path: 'para-ti', component: ParaTiComponent},
  { path: 'buscar', component: BuscarComponent},
  { path: 'siguiendo', component: SiguiendoComponent},
  { path: 'perfil', component: PerfilComponent},
  { path: 'subir-episodio', component: SubirEpisodioComponent},
  { path: 'reproductor', component:ReproductorComponent},
  { path: 'podcast', component:PaginaPodcastComponent},
  { path: 'creador',component:PaginaCreadorComponent},
  { path: 'contrasenia',component:RecuperarContraseniaComponent},
  { path: 'gestion-usuarios',component:GestionUsuariosComponent},
  { path: 'gestion-creadores',component:GestionCreadoresComponent},
  { path: 'gestion-podcasts',component:GestionPodcastsComponent},
  { path: 'gestion-episodios',component:GestionEpisodiosComponent},
];

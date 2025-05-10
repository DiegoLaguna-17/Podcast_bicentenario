import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component'; // Tu componente raíz standalone
import { provideRouter } from '@angular/router'; // Si usas enrutamiento
import { routes } from './app/app.routes'; // Tus rutas
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http'; // Importa provideHttpClient

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes), // Ejemplo si tienes rutas
    provideHttpClient(withInterceptorsFromDi()), // Configura HttpClient aquí
    // Otros providers globales que necesites
  ]
}).catch(err => console.error(err));
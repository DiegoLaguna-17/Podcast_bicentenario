// registrar.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Service {
  private apiUrl = 'http://127.0.0.1:8000/';  // Ajusta esta URL

  constructor(private http: HttpClient) { }

  registrar(datos: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
    return this.http.post(this.apiUrl, JSON.stringify(datos), { headers });
  }
}
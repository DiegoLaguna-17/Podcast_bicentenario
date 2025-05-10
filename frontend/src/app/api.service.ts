import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root' // Esto funciona perfectamente en standalone
})
export class ApiService {

  private baseUrl = 'http://127.0.0.1:8000/'; // URL base de tu API Django

  constructor(private http: HttpClient) { }

  getItems(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}items/`);
  }

  resgitarCreador(item: any): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
      })
    };
    return this.http.post<any>(`${this.baseUrl}registro`, item, httpOptions);
  }

  // api.service.ts
login(formData: FormData): Observable<any> {
  return this.http.post(`${this.baseUrl}login/`, formData);
  // No necesitas headers para FormData
}

  // ... otros métodos (getItemById, updateItem, deleteItem)
}
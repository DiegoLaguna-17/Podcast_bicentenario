import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private userDataSource = new BehaviorSubject<any>(null);
  userData$ = this.userDataSource.asObservable();

  // Nuevo subject específico para el ID de creación
  private creatorIdSource = new BehaviorSubject<number | null>(null);
  creatorId$ = this.creatorIdSource.asObservable();

  setUserData(datos: any) {
    this.userDataSource.next(datos);
  }

  setCreatorId(id: number) {
    this.creatorIdSource.next(id);
  }
}
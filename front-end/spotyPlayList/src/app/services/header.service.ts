import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class HeaderService {
  constructor() {}
  // Obersable que va cambiando el contenido del header segun la ruta
  private headerSubject = new BehaviorSubject<string>('SpotyPlayList');
  // Metodo para emitir el valor del header
  emitHeader(value: string): void {
    this.headerSubject.next(value);
  }
  // Observable para exponer el valor del header
  header$: Observable<string> = this.headerSubject.asObservable();
  // Funcion para actualizar el header
  updateHeader(value: string): void {
    this.emitHeader(value);
  }
}

import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class LanguageService {
  private languageSubject = new BehaviorSubject<string>('en'); // Idioma por defecto: inglés
  language$ = this.languageSubject.asObservable();

  setLanguage(language: string): void {
    this.languageSubject.next(language); // Cambia el idioma
  }

  getLanguage(): string {
    return this.languageSubject.getValue(); // Obtiene el idioma actual
  }
}

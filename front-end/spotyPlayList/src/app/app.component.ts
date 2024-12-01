import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { environment } from '../environments/environment';
import { HeaderService } from './services/header.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  headerText: string = 'SpotyPlayList';
  title = 'spotyPlayList';

  constructor(
    private headerService: HeaderService,
    private cdr: ChangeDetectorRef
  ) {}

  // funcion login que llama la url http://localhost:5000/login
  login() {
    window.location.href = `${environment.apiUrl}/login`;
  }

  // Método que maneja el callback después de la autenticación
  ngOnInit() {
    this.textHeader();
  }

  // Función para actualizar la variable headerText con el valor del header
  textHeader() {
    this.headerService.header$.subscribe((header) => {
      this.headerText = header;
      this.cdr.detectChanges(); // Forzar la detección de cambios
    });
  }
}
